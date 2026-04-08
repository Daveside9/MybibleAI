#!/usr/bin/env python3
"""
Setup Real Live Matches using Free APIs
This script fetches real live match data and updates your database
"""
import asyncio
import httpx
import os
from datetime import datetime, date
from app.core.database import SessionLocal
from app.models.match import Match, MatchStatus

class FootballDataAPI:
    """Free Football-Data.org API client"""
    
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://api.football-data.org/v4"
        self.headers = {"X-Auth-Token": token}
    
    async def get_live_matches(self):
        """Get currently live matches"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/matches",
                    headers=self.headers,
                    params={"status": "LIVE"}
                )
                if response.status_code == 200:
                    data = response.json()
                    return data.get("matches", [])
                else:
                    print(f"❌ API Error: {response.status_code}")
                    print(f"Response: {response.text}")
            except Exception as e:
                print(f"❌ Request failed: {e}")
        return []
    
    async def get_todays_matches(self):
        """Get today's matches"""
        today = date.today().isoformat()
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/matches",
                    headers=self.headers,
                    params={"dateFrom": today, "dateTo": today}
                )
                if response.status_code == 200:
                    data = response.json()
                    return data.get("matches", [])
                else:
                    print(f"❌ API Error: {response.status_code}")
            except Exception as e:
                print(f"❌ Request failed: {e}")
        return []

class ESPNSoccerAPI:
    """Free ESPN Soccer API (no key required)"""
    
    def __init__(self):
        self.base_url = "https://site.api.espn.com/apis/site/v2/sports/soccer"
    
    async def get_live_matches(self):
        """Get live matches from ESPN"""
        leagues = [
            "eng.1",  # Premier League
            "esp.1",  # La Liga
            "ger.1",  # Bundesliga
            "ita.1",  # Serie A
            "fra.1",  # Ligue 1
        ]
        
        all_matches = []
        
        async with httpx.AsyncClient() as client:
            for league in leagues:
                try:
                    response = await client.get(f"{self.base_url}/{league}/scoreboard")
                    if response.status_code == 200:
                        data = response.json()
                        for event in data.get("events", []):
                            status = event.get("status", {}).get("type", {}).get("name", "")
                            if "IN_PROGRESS" in status or "HALFTIME" in status:
                                all_matches.append({
                                    "id": event.get("id"),
                                    "name": event.get("name"),
                                    "shortName": event.get("shortName"),
                                    "status": status,
                                    "league": league,
                                    "competitions": event.get("competitions", [{}])[0],
                                    "date": event.get("date")
                                })
                except Exception as e:
                    print(f"❌ ESPN API error for {league}: {e}")
        
        return all_matches

def convert_football_data_match(match_data):
    """Convert Football-Data.org match to our format"""
    home_team = match_data.get("homeTeam", {}).get("name", "Unknown")
    away_team = match_data.get("awayTeam", {}).get("name", "Unknown")
    
    # Map status
    status_map = {
        "LIVE": MatchStatus.LIVE,
        "IN_PLAY": MatchStatus.LIVE,
        "PAUSED": MatchStatus.LIVE,
        "FINISHED": MatchStatus.FINISHED,
        "SCHEDULED": MatchStatus.SCHEDULED,
        "POSTPONED": MatchStatus.POSTPONED,
        "CANCELLED": MatchStatus.CANCELLED
    }
    
    api_status = match_data.get("status", "SCHEDULED")
    our_status = status_map.get(api_status, MatchStatus.SCHEDULED)
    
    return {
        "external_id": match_data.get("id"),
        "title": f"{home_team} vs {away_team}",
        "home_team": home_team,
        "away_team": away_team,
        "home_score": match_data.get("score", {}).get("fullTime", {}).get("home") or 0,
        "away_score": match_data.get("score", {}).get("fullTime", {}).get("away") or 0,
        "status": our_status,
        "scheduled_at": datetime.fromisoformat(match_data.get("utcDate", "").replace("Z", "+00:00")),
        "league_name": match_data.get("competition", {}).get("name", "Unknown League")
    }

def convert_espn_match(match_data):
    """Convert ESPN match to our format"""
    competitions = match_data.get("competitions", [{}])[0]
    competitors = competitions.get("competitors", [])
    
    if len(competitors) >= 2:
        home_team = competitors[0].get("team", {}).get("displayName", "Unknown")
        away_team = competitors[1].get("team", {}).get("displayName", "Unknown")
        home_score = int(competitors[0].get("score", 0))
        away_score = int(competitors[1].get("score", 0))
    else:
        home_team = "Unknown"
        away_team = "Unknown"
        home_score = 0
        away_score = 0
    
    return {
        "external_id": int(match_data.get("id", 0)),
        "title": match_data.get("name", f"{home_team} vs {away_team}"),
        "home_team": home_team,
        "away_team": away_team,
        "home_score": home_score,
        "away_score": away_score,
        "status": MatchStatus.LIVE,
        "scheduled_at": datetime.fromisoformat(match_data.get("date", "").replace("Z", "+00:00")) if match_data.get("date") else datetime.utcnow(),
        "league_name": match_data.get("league", "ESPN League")
    }

async def setup_real_live_matches():
    """Main function to setup real live matches"""
    
    print("🔴 Setting up Real Live Matches")
    print("=" * 50)
    
    db = SessionLocal()
    
    try:
        # Option 1: Try Football-Data.org (if token available)
        football_data_token = os.getenv("FOOTBALL_DATA_TOKEN")
        if football_data_token:
            print("⚽ Using Football-Data.org API...")
            api = FootballDataAPI(football_data_token)
            
            # Get live matches
            live_matches = await api.get_live_matches()
            print(f"Found {len(live_matches)} live matches from Football-Data.org")
            
            for match_data in live_matches:
                match_info = convert_football_data_match(match_data)
                
                # Check if match already exists
                existing = db.query(Match).filter(Match.external_id == match_info["external_id"]).first()
                
                if existing:
                    # Update existing match
                    for key, value in match_info.items():
                        if key != "external_id":
                            setattr(existing, key, value)
                    print(f"✅ Updated: {match_info['title']}")
                else:
                    # Create new match
                    new_match = Match(**match_info)
                    db.add(new_match)
                    print(f"✅ Added: {match_info['title']}")
        
        # Option 2: ESPN API (always free, no key needed)
        else:
            print("📺 Using ESPN Soccer API (free, no key required)...")
            espn_api = ESPNSoccerAPI()
            
            live_matches = await espn_api.get_live_matches()
            print(f"Found {len(live_matches)} live matches from ESPN")
            
            for match_data in live_matches:
                match_info = convert_espn_match(match_data)
                
                # Check if match already exists
                existing = db.query(Match).filter(Match.external_id == match_info["external_id"]).first()
                
                if existing:
                    # Update existing match
                    for key, value in match_info.items():
                        if key != "external_id":
                            setattr(existing, key, value)
                    print(f"✅ Updated: {match_info['title']}")
                else:
                    # Create new match
                    new_match = Match(**match_info)
                    db.add(new_match)
                    print(f"✅ Added: {match_info['title']}")
        
        db.commit()
        
        # Show summary
        live_count = db.query(Match).filter(Match.status == MatchStatus.LIVE).count()
        total_count = db.query(Match).count()
        
        print(f"\n📊 Database Summary:")
        print(f"   • Live matches: {live_count}")
        print(f"   • Total matches: {total_count}")
        
        if live_count > 0:
            print(f"\n🎬 Ready to test live streaming!")
            print(f"   1. Visit: http://localhost:3000")
            print(f"   2. Navigate to any live match")
            print(f"   3. Enjoy real live match data!")
        else:
            print(f"\n⏰ No live matches found right now.")
            print(f"   This is normal - try again during match hours!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

def show_setup_instructions():
    """Show setup instructions for free APIs"""
    
    print("🆓 Free Live Match API Setup")
    print("=" * 40)
    print()
    print("Option 1: Football-Data.org (Recommended)")
    print("1. Go to: https://www.football-data.org/client/register")
    print("2. Register for FREE (no credit card required)")
    print("3. Get your API token")
    print("4. Add to .env file:")
    print("   FOOTBALL_DATA_TOKEN=your_token_here")
    print()
    print("Option 2: ESPN API (No registration needed)")
    print("✅ Already configured - just run the script!")
    print()
    print("To run: python setup_real_live_matches.py")

if __name__ == "__main__":
    # Check if we have any API credentials
    football_data_token = os.getenv("FOOTBALL_DATA_TOKEN")
    
    if not football_data_token:
        print("⚠️  No Football-Data.org token found")
        print("🔄 Will use ESPN API instead (free, no setup required)")
        print()
    
    asyncio.run(setup_real_live_matches())