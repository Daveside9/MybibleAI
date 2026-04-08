#!/usr/bin/env python3
"""
Fetch real-time matches for all leagues using ESPN API
"""
import asyncio
import httpx
import sys
import os
from datetime import datetime, date, timedelta

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.match import Match, MatchStatus

async def fetch_matches_for_all_leagues():
    """Fetch real matches from ESPN API for multiple leagues"""
    
    print("🏆 Fetching Real Matches for All Leagues...")
    print("=" * 60)
    
    # ESPN league mappings (ESPN ID -> League DB ID, Name)
    espn_leagues = [
        # Major European Leagues
        ("eng.1", 1, "Premier League"),
        ("esp.1", 2, "La Liga"), 
        ("ger.1", 9, "Bundesliga"),
        ("ita.1", 8, "Serie A"),
        ("fra.1", 10, "Ligue 1"),
        ("ned.1", 11, "Eredivisie"),
        ("por.1", 12, "Primeira Liga"),
        
        # International Competitions
        ("uefa.champions", 3, "Champions League"),
        ("uefa.europa", 7, "Europa League"),
        ("uefa.nations", 13, "UEFA Nations League"),
        
        # Other Popular Leagues
        ("usa.1", 15, "MLS"),
        ("mex.1", 16, "Liga MX"),
        ("bra.1", 17, "Brazilian Serie A"),
        ("arg.1", 18, "Argentine Primera"),
        ("bel.1", 19, "Belgian Pro League"),
        ("sco.1", 22, "Scottish Premiership"),
        ("tur.1", 23, "Turkish Super Lig"),
        
        # Asian Leagues
        ("jpn.1", 27, "J1 League"),
        ("kor.1", 28, "K League 1"),
    ]
    
    total_matches_added = 0
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        for espn_id, league_db_id, league_name in espn_leagues:
            print(f"\n📺 Fetching {league_name}...")
            
            try:
                # Fetch matches from ESPN
                matches = await fetch_espn_matches(client, espn_id, league_name)
                
                if matches:
                    # Save to database
                    saved_count = save_matches_to_db(matches, league_db_id, league_name)
                    total_matches_added += saved_count
                    print(f"  ✅ Saved {saved_count} matches for {league_name}")
                else:
                    print(f"  ⚠️  No matches found for {league_name}")
                    
            except Exception as e:
                print(f"  ❌ Error fetching {league_name}: {e}")
    
    print(f"\n🎉 COMPLETED! Added {total_matches_added} total matches across all leagues!")
    return total_matches_added

async def fetch_espn_matches(client, league_id, league_name):
    """Fetch matches from ESPN API for a specific league"""
    
    matches = []
    
    # Try different date ranges to get more matches
    date_ranges = [
        (0, 7),    # Next 7 days
        (7, 14),   # Days 7-14
        (14, 21),  # Days 14-21
        (-7, 0),   # Last 7 days (for live/recent matches)
    ]
    
    for start_offset, end_offset in date_ranges:
        start_date = (datetime.now() + timedelta(days=start_offset)).strftime('%Y%m%d')
        end_date = (datetime.now() + timedelta(days=end_offset)).strftime('%Y%m%d')
        
        url = f"https://site.api.espn.com/apis/site/v2/sports/soccer/{league_id}/scoreboard"
        params = {
            'dates': f"{start_date}-{end_date}",
            'limit': 100
        }
        
        try:
            response = await client.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                events = data.get('events', [])
                matches.extend(events)
                print(f"    Found {len(events)} matches for {start_date}-{end_date}")
            else:
                print(f"    Error {response.status_code} for {start_date}-{end_date}")
                
        except Exception as e:
            print(f"    Error fetching {start_date}-{end_date}: {e}")
    
    # Remove duplicates based on ESPN ID
    unique_matches = {}
    for match in matches:
        match_id = match.get('id')
        if match_id and match_id not in unique_matches:
            unique_matches[match_id] = match
    
    return list(unique_matches.values())

def save_matches_to_db(matches, league_db_id, league_name):
    """Save matches to database"""
    
    db = SessionLocal()
    saved_count = 0
    
    try:
        for match_data in matches:
            # Extract match details
            match_id = match_data.get('id')
            if not match_id:
                continue
            
            # Check if match already exists
            existing = db.query(Match).filter(Match.external_id == int(match_id)).first()
            if existing:
                continue
            
            # Get team names
            competitions = match_data.get('competitions', [])
            if not competitions:
                continue
                
            competitors = competitions[0].get('competitors', [])
            if len(competitors) < 2:
                continue
            
            home_team = competitors[0].get('team', {}).get('displayName', 'Unknown')
            away_team = competitors[1].get('team', {}).get('displayName', 'Unknown')
            title = f"{home_team} vs {away_team}"
            
            # Parse date
            date_str = match_data.get('date')
            if date_str:
                scheduled_at = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            else:
                scheduled_at = datetime.now()
            
            # Determine status
            status_type = match_data.get('status', {}).get('type', {}).get('name', 'scheduled')
            if status_type.lower() in ['pre', 'scheduled']:
                status = MatchStatus.SCHEDULED
            elif status_type.lower() in ['in', 'live']:
                status = MatchStatus.LIVE
            elif status_type.lower() in ['post', 'final']:
                status = MatchStatus.FINISHED
            else:
                status = MatchStatus.SCHEDULED
            
            # Get scores
            home_score = None
            away_score = None
            
            if competitors:
                home_score = competitors[0].get('score')
                away_score = competitors[1].get('score')
            
            # Create match
            match = Match(
                external_id=int(match_id),
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
        print(f"  Error saving matches for {league_name}: {e}")
        db.rollback()
        return 0
    finally:
        db.close()

def main():
    """Main function"""
    asyncio.run(fetch_matches_for_all_leagues())

if __name__ == "__main__":
    main()