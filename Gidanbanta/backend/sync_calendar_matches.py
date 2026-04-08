#!/usr/bin/env python3
"""
Comprehensive Match Calendar Sync Script
Fetches real-time matches and properly organizes them by date and league
"""

import requests
import json
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./gidanbanta.db")
engine = create_engine(DATABASE_URL)

# Import models after engine setup
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models.match import Match, MatchStatus, League
from app.core.database import get_db

def fetch_espn_matches():
    """Fetch matches from ESPN API for multiple leagues and dates"""
    
    # ESPN league IDs for major competitions
    leagues = {
        'eng.1': 'Premier League',
        'esp.1': 'La Liga', 
        'ger.1': 'Bundesliga',
        'ita.1': 'Serie A',
        'fra.1': 'Ligue 1',
        'uefa.champions': 'UEFA Champions League',
        'uefa.europa': 'UEFA Europa League',
        'ned.1': 'Eredivisie',
        'por.1': 'Primeira Liga',
        'bel.1': 'Belgian Pro League'
    }
    
    all_matches = []
    
    # Get matches for next 7 days
    for days_ahead in range(0, 8):
        target_date = datetime.now() + timedelta(days=days_ahead)
        date_str = target_date.strftime('%Y%m%d')
        
        print(f"Fetching matches for {target_date.strftime('%Y-%m-%d')}...")
        
        for league_id, league_name in leagues.items():
            try:
                url = f"https://site.api.espn.com/apis/site/v2/sports/soccer/{league_id}/scoreboard"
                params = {
                    'dates': date_str,
                    'limit': 50
                }
                
                response = requests.get(url, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if 'events' in data:
                        for event in data['events']:
                            try:
                                # Parse match data
                                match_data = {
                                    'external_id': int(event['id']),
                                    'league_name': league_name,
                                    'league_id': league_id,
                                    'home_team': event['competitions'][0]['competitors'][0]['team']['displayName'],
                                    'away_team': event['competitions'][0]['competitors'][1]['team']['displayName'],
                                    'scheduled_time': event['date'],
                                    'status': event['status']['type']['name'].lower(),
                                    'home_score': None,
                                    'away_score': None
                                }
                                
                                # Get scores if available
                                competitors = event['competitions'][0]['competitors']
                                if competitors[0].get('score') and competitors[1].get('score'):
                                    match_data['home_score'] = int(competitors[0]['score'])
                                    match_data['away_score'] = int(competitors[1]['score'])
                                
                                # Generate realistic odds
                                import random
                                match_data['home_odds'] = round(random.uniform(1.5, 4.0), 2)
                                match_data['draw_odds'] = round(random.uniform(2.8, 4.5), 2)
                                match_data['away_odds'] = round(random.uniform(1.5, 4.0), 2)
                                
                                all_matches.append(match_data)
                                
                            except (KeyError, ValueError, IndexError) as e:
                                print(f"Error parsing match data: {e}")
                                continue
                                
                else:
                    print(f"Failed to fetch {league_name} for {date_str}: {response.status_code}")
                    
            except requests.RequestException as e:
                print(f"Request error for {league_name}: {e}")
                continue
    
    return all_matches

def sync_leagues_to_db(db: Session, matches_data):
    """Ensure all leagues exist in database"""
    
    league_mapping = {}
    unique_leagues = set((match['league_name'], match['league_id']) for match in matches_data)
    
    for league_name, league_espn_id in unique_leagues:
        # Check if league exists
        existing_league = db.query(League).filter(League.name == league_name).first()
        
        if not existing_league:
            # Create new league
            new_league = League(
                name=league_name,
                country=get_country_from_league(league_name),
                external_id=league_espn_id,
                priority=get_league_priority(league_name)
            )
            db.add(new_league)
            db.commit()
            db.refresh(new_league)
            league_mapping[league_name] = new_league.id
            print(f"Created league: {league_name}")
        else:
            league_mapping[league_name] = existing_league.id
    
    return league_mapping

def get_country_from_league(league_name):
    """Map league names to countries"""
    country_map = {
        'Premier League': 'England',
        'La Liga': 'Spain',
        'Bundesliga': 'Germany', 
        'Serie A': 'Italy',
        'Ligue 1': 'France',
        'UEFA Champions League': 'Europe',
        'UEFA Europa League': 'Europe',
        'Eredivisie': 'Netherlands',
        'Primeira Liga': 'Portugal',
        'Belgian Pro League': 'Belgium'
    }
    return country_map.get(league_name, 'International')

def get_league_priority(league_name):
    """Assign priority to leagues"""
    priority_map = {
        'UEFA Champions League': 100,
        'Premier League': 90,
        'La Liga': 85,
        'Bundesliga': 80,
        'Serie A': 75,
        'Ligue 1': 70,
        'UEFA Europa League': 65,
        'Eredivisie': 60,
        'Primeira Liga': 55,
        'Belgian Pro League': 50
    }
    return priority_map.get(league_name, 40)

def sync_matches_to_db(db: Session, matches_data, league_mapping):
    """Sync matches to database with proper calendar organization"""
    
    synced_count = 0
    updated_count = 0
    
    for match_data in matches_data:
        try:
            # Parse scheduled time
            scheduled_dt = datetime.fromisoformat(match_data['scheduled_time'].replace('Z', '+00:00'))
            
            # Check if match already exists
            existing_match = db.query(Match).filter(
                Match.external_id == match_data['external_id']
            ).first()
            
            league_id = league_mapping.get(match_data['league_name'])
            if not league_id:
                print(f"League not found: {match_data['league_name']}")
                continue
            
            if existing_match:
                # Update existing match
                existing_match.scheduled_at = scheduled_dt
                existing_match.league_id = league_id
                existing_match.status = MatchStatus.SCHEDULED if match_data['status'] == 'scheduled' else MatchStatus.LIVE
                existing_match.home_odds = match_data['home_odds']
                existing_match.draw_odds = match_data['draw_odds'] 
                existing_match.away_odds = match_data['away_odds']
                
                # Update scores if available
                if match_data['home_score'] is not None:
                    existing_match.home_score = match_data['home_score']
                    existing_match.away_score = match_data['away_score']
                    existing_match.status = MatchStatus.FINISHED
                
                updated_count += 1
            else:
                # Create new match
                new_match = Match(
                    external_id=match_data['external_id'],
                    title=f"{match_data['home_team']} vs {match_data['away_team']}",
                    home_team=match_data['home_team'],
                    away_team=match_data['away_team'],
                    scheduled_at=scheduled_dt,
                    league_id=league_id,
                    status=MatchStatus.SCHEDULED if match_data['status'] == 'scheduled' else MatchStatus.LIVE,
                    home_odds=match_data['home_odds'],
                    draw_odds=match_data['draw_odds'],
                    away_odds=match_data['away_odds'],
                    home_score=match_data['home_score'],
                    away_score=match_data['away_score'],
                    is_featured=True  # Mark real matches as featured
                )
                
                db.add(new_match)
                synced_count += 1
                
        except Exception as e:
            print(f"Error syncing match {match_data.get('external_id', 'unknown')}: {e}")
            continue
    
    db.commit()
    return synced_count, updated_count

def clean_old_matches(db: Session):
    """Remove old finished matches and invalid data"""
    
    # Remove matches older than 7 days
    cutoff_date = datetime.now() - timedelta(days=7)
    
    old_matches = db.query(Match).filter(
        Match.scheduled_at < cutoff_date,
        Match.status == MatchStatus.FINISHED
    ).delete()
    
    # Remove matches without external_id (mock data)
    mock_matches = db.query(Match).filter(
        (Match.external_id.is_(None)) | (Match.external_id == 0)
    ).delete()
    
    db.commit()
    
    return old_matches, mock_matches

def main():
    """Main sync function"""
    print("🚀 Starting comprehensive match calendar sync...")
    
    # Create database session
    db = next(get_db())
    
    try:
        # Step 1: Fetch fresh match data
        print("📡 Fetching real-time match data from ESPN...")
        matches_data = fetch_espn_matches()
        print(f"✅ Fetched {len(matches_data)} matches")
        
        if not matches_data:
            print("❌ No matches fetched. Exiting.")
            return
        
        # Step 2: Sync leagues
        print("🏆 Syncing leagues to database...")
        league_mapping = sync_leagues_to_db(db, matches_data)
        print(f"✅ Synced {len(league_mapping)} leagues")
        
        # Step 3: Clean old data
        print("🧹 Cleaning old matches...")
        old_count, mock_count = clean_old_matches(db)
        print(f"✅ Removed {old_count} old matches and {mock_count} mock matches")
        
        # Step 4: Sync matches
        print("⚽ Syncing matches to database...")
        synced_count, updated_count = sync_matches_to_db(db, matches_data, league_mapping)
        print(f"✅ Synced {synced_count} new matches, updated {updated_count} existing matches")
        
        # Step 5: Summary
        total_matches = db.query(Match).filter(Match.external_id > 0).count()
        print(f"\n🎉 Sync completed successfully!")
        print(f"📊 Total real matches in database: {total_matches}")
        print(f"📅 Matches organized by proper calendar dates and leagues")
        
    except Exception as e:
        print(f"❌ Sync failed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()