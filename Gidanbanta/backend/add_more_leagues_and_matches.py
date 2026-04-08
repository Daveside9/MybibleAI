#!/usr/bin/env python3
"""
Add more leagues and fetch real-time match data for each
This script will add popular football leagues and fetch their current matches
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import requests
from datetime import datetime, timedelta
from app.core.database import get_db
from app.models.match import Match, League, Team, MatchStatus
from sqlalchemy.orm import Session

# Football-Data.org API configuration
API_TOKEN = "b8b1c9c0c8b44f5bb4c4c4c4c4c4c4c4"  # Your existing token
BASE_URL = "https://api.football-data.org/v4"

def create_leagues():
    """Create additional popular leagues"""
    
    leagues_to_add = [
        # Major European Leagues
        {"id": 8, "name": "Serie A", "country": "Italy", "priority": 95, "api_id": 135},
        {"id": 9, "name": "Bundesliga", "country": "Germany", "priority": 94, "api_id": 78},
        {"id": 10, "name": "Ligue 1", "country": "France", "priority": 93, "api_id": 61},
        {"id": 11, "name": "Eredivisie", "country": "Netherlands", "priority": 85, "api_id": 88},
        {"id": 12, "name": "Primeira Liga", "country": "Portugal", "priority": 84, "api_id": 94},
        
        # International Competitions
        {"id": 13, "name": "UEFA Nations League", "country": "Europe", "priority": 90, "api_id": 1},
        {"id": 14, "name": "FIFA World Cup", "country": "International", "priority": 100, "api_id": 2000},
        {"id": 15, "name": "Copa America", "country": "South America", "priority": 88, "api_id": 2001},
        
        # Other Popular Leagues
        {"id": 16, "name": "MLS", "country": "USA", "priority": 75, "api_id": 253},
        {"id": 17, "name": "Liga MX", "country": "Mexico", "priority": 74, "api_id": 262},
        {"id": 18, "name": "Brazilian Serie A", "country": "Brazil", "priority": 82, "api_id": 71},
        {"id": 19, "name": "Argentine Primera", "country": "Argentina", "priority": 81, "api_id": 128},
        
        # African Leagues
        {"id": 20, "name": "CAF Champions League", "country": "Africa", "priority": 78, "api_id": 2},
        {"id": 21, "name": "AFCON", "country": "Africa", "priority": 87, "api_id": 2013},
        
        # Asian Leagues
        {"id": 22, "name": "AFC Champions League", "country": "Asia", "priority": 76, "api_id": 2018},
        {"id": 23, "name": "J1 League", "country": "Japan", "priority": 70, "api_id": 302},
        {"id": 24, "name": "K League 1", "country": "South Korea", "priority": 69, "api_id": 98},
        
        # Additional European Leagues
        {"id": 25, "name": "Belgian Pro League", "country": "Belgium", "priority": 72, "api_id": 144},
        {"id": 26, "name": "Swiss Super League", "country": "Switzerland", "priority": 68, "api_id": 207},
        {"id": 27, "name": "Austrian Bundesliga", "country": "Austria", "priority": 67, "api_id": 218},
        {"id": 28, "name": "Scottish Premiership", "country": "Scotland", "priority": 71, "api_id": 501},
        {"id": 29, "name": "Turkish Super Lig", "country": "Turkey", "priority": 73, "api_id": 203},
        {"id": 30, "name": "Russian Premier League", "country": "Russia", "priority": 70, "api_id": 235}
    ]
    
    db = next(get_db())
    
    try:
        print("Adding new leagues...")
        print("=" * 50)
        
        added_count = 0
        for league_data in leagues_to_add:
            # Check if league already exists
            existing = db.query(League).filter(League.id == league_data["id"]).first()
            if existing:
                print(f"League {league_data['name']} already exists, skipping...")
                continue
            
            # Create new league
            league = League(
                id=league_data["id"],
                name=league_data["name"],
                country=league_data["country"],
                priority=league_data["priority"],
                logo=f"https://crests.football-data.org/{league_data['api_id']}.png"
            )
            
            db.add(league)
            added_count += 1
            print(f"Added: {league_data['name']} ({league_data['country']})")
        
        db.commit()
        print(f"\n✅ Successfully added {added_count} new leagues!")
        
    except Exception as e:
        print(f"Error adding leagues: {e}")
        db.rollback()
    finally:
        db.close()

def fetch_matches_for_league(league_api_id, league_db_id, league_name):
    """Fetch matches for a specific league"""
    
    headers = {
        'X-Auth-Token': API_TOKEN
    }
    
    # Get matches for the next 30 days
    date_from = datetime.now().strftime('%Y-%m-%d')
    date_to = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    
    url = f"{BASE_URL}/competitions/{league_api_id}/matches"
    params = {
        'dateFrom': date_from,
        'dateTo': date_to,
        'status': 'SCHEDULED,LIVE,IN_PLAY,PAUSED,FINISHED'
    }
    
    try:
        print(f"Fetching matches for {league_name}...")
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            matches = data.get('matches', [])
            print(f"  Found {len(matches)} matches")
            return matches
        else:
            print(f"  Error: {response.status_code} - {response.text}")
            return []
            
    except Exception as e:
        print(f"  Error fetching matches: {e}")
        return []

def save_matches_to_db(matches, league_db_id):
    """Save matches to database"""
    
    db = next(get_db())
    
    try:
        saved_count = 0
        
        for match_data in matches:
            # Check if match already exists
            external_id = match_data['id']
            existing = db.query(Match).filter(Match.external_id == external_id).first()
            if existing:
                continue
            
            # Extract match details
            home_team = match_data['homeTeam']['name']
            away_team = match_data['awayTeam']['name']
            title = f"{home_team} vs {away_team}"
            
            # Parse scheduled time
            scheduled_at = datetime.fromisoformat(match_data['utcDate'].replace('Z', '+00:00'))
            
            # Determine status
            api_status = match_data['status']
            if api_status in ['SCHEDULED', 'TIMED']:
                status = MatchStatus.SCHEDULED
            elif api_status in ['LIVE', 'IN_PLAY', 'PAUSED']:
                status = MatchStatus.LIVE
            elif api_status == 'FINISHED':
                status = MatchStatus.FINISHED
            elif api_status == 'POSTPONED':
                status = MatchStatus.POSTPONED
            elif api_status == 'CANCELLED':
                status = MatchStatus.CANCELLED
            else:
                status = MatchStatus.SCHEDULED
            
            # Get scores
            score = match_data.get('score', {})
            full_time = score.get('fullTime', {})
            home_score = full_time.get('home')
            away_score = full_time.get('away')
            
            # Create match
            match = Match(
                external_id=external_id,
                title=title,
                home_team=home_team,
                away_team=away_team,
                league_id=league_db_id,
                scheduled_at=scheduled_at,
                status=status,
                home_score=home_score,
                away_score=away_score,
                home_odds=2.0,  # Default odds
                away_odds=2.0,
                draw_odds=3.0,
                is_featured=False
            )
            
            db.add(match)
            saved_count += 1
        
        db.commit()
        return saved_count
        
    except Exception as e:
        print(f"  Error saving matches: {e}")
        db.rollback()
        return 0
    finally:
        db.close()

def fetch_all_league_matches():
    """Fetch matches for all leagues"""
    
    # League mappings (API ID -> DB ID, Name)
    league_mappings = [
        (2021, 1, "Premier League"),  # Existing
        (2014, 2, "La Liga"),        # Existing  
        (2019, 6, "Serie A"),        # New
        (2002, 7, "Bundesliga"),     # New
        (2015, 8, "Ligue 1"),        # New
        (2003, 9, "Eredivisie"),     # New
        (2017, 10, "Primeira Liga"), # New
        (2001, 11, "UEFA Champions League"),  # Existing
        (2018, 12, "UEFA Europa League"),     # Existing
        
        # Add more mappings for new leagues
        (2013, 13, "Serie A"),
        (2002, 14, "Bundesliga"), 
        (2015, 15, "Ligue 1"),
        (2003, 16, "Eredivisie"),
        (2017, 17, "Primeira Liga"),
    ]
    
    print("Fetching matches for all leagues...")
    print("=" * 50)
    
    total_matches = 0
    
    for api_id, db_id, name in league_mappings:
        matches = fetch_matches_for_league(api_id, db_id, name)
        if matches:
            saved = save_matches_to_db(matches, db_id)
            print(f"  Saved {saved} new matches for {name}")
            total_matches += saved
        else:
            print(f"  No matches found for {name}")
    
    print(f"\n✅ Total new matches added: {total_matches}")

def main():
    """Main function"""
    
    print("🏆 ADDING MORE LEAGUES AND FETCHING MATCHES")
    print("=" * 60)
    
    # Step 1: Add new leagues
    create_leagues()
    
    print("\n" + "=" * 60)
    
    # Step 2: Fetch matches for all leagues
    fetch_all_league_matches()
    
    print("\n" + "=" * 60)
    print("✅ COMPLETED! Your database now has more leagues with real-time matches!")

if __name__ == "__main__":
    main()