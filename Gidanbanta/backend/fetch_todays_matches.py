#!/usr/bin/env python3
"""
Fetch Today's Real Matches - Including Real Madrid vs Manchester City
This script searches for specific matches happening today
"""
import asyncio
import httpx
import os
from datetime import datetime, date, timedelta
from app.core.database import SessionLocal
from app.models.match import Match, MatchStatus

class ComprehensiveMatchFetcher:
    """Fetch matches from multiple free APIs"""
    
    def __init__(self):
        self.football_data_token = os.getenv("FOOTBALL_DATA_TOKEN")
        self.matches_found = []
    
    async def search_football_data_org(self, target_teams=None):
        """Search Football-Data.org for today's matches"""
        if not self.football_data_token:
            print("⚠️  No Football-Data.org token - skipping this API")
            return []
        
        print("⚽ Searching Football-Data.org...")
        
        # Search for matches in the next few days
        today = date.today()
        tomorrow = today + timedelta(days=1)
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    "https://api.football-data.org/v4/matches",
                    headers={"X-Auth-Token": self.football_data_token},
                    params={
                        "dateFrom": today.isoformat(),
                        "dateTo": tomorrow.isoformat()
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    matches = data.get("matches", [])
                    
                    print(f"   Found {len(matches)} matches from Football-Data.org")
                    
                    # Filter for target teams if specified
                    if target_teams:
                        filtered_matches = []
                        for match in matches:
                            home_team = match.get("homeTeam", {}).get("name", "").lower()
                            away_team = match.get("awayTeam", {}).get("name", "").lower()
                            
                            for target in target_teams:
                                if target.lower() in home_team or target.lower() in away_team:
                                    filtered_matches.append(match)
                                    break
                        
                        print(f"   Filtered to {len(filtered_matches)} matches with target teams")
                        return filtered_matches
                    
                    return matches
                else:
                    print(f"   ❌ API Error: {response.status_code}")
                    print(f"   Response: {response.text}")
            except Exception as e:
                print(f"   ❌ Request failed: {e}")
        
        return []
    
    async def search_espn_api(self, target_teams=None):
        """Search ESPN API for today's matches"""
        print("📺 Searching ESPN Soccer API...")
        
        leagues = [
            ("eng.1", "Premier League"),
            ("esp.1", "La Liga"),
            ("ger.1", "Bundesliga"),
            ("ita.1", "Serie A"),
            ("fra.1", "Ligue 1"),
            ("uefa.champions", "Champions League"),
            ("uefa.europa", "Europa League"),
        ]
        
        all_matches = []
        
        async with httpx.AsyncClient() as client:
            for league_id, league_name in leagues:
                try:
                    response = await client.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{league_id}/scoreboard")
                    
                    if response.status_code == 200:
                        data = response.json()
                        events = data.get("events", [])
                        
                        for event in events:
                            # Check if match is today or live
                            event_date = event.get("date", "")
                            if event_date:
                                match_date = datetime.fromisoformat(event_date.replace("Z", "+00:00")).date()
                                if match_date != date.today():
                                    continue
                            
                            # Get team names
                            competitions = event.get("competitions", [{}])
                            if competitions:
                                competitors = competitions[0].get("competitors", [])
                                if len(competitors) >= 2:
                                    home_team = competitors[0].get("team", {}).get("displayName", "")
                                    away_team = competitors[1].get("team", {}).get("displayName", "")
                                    
                                    # Filter for target teams if specified
                                    if target_teams:
                                        found_target = False
                                        for target in target_teams:
                                            if (target.lower() in home_team.lower() or 
                                                target.lower() in away_team.lower()):
                                                found_target = True
                                                break
                                        
                                        if not found_target:
                                            continue
                                    
                                    match_info = {
                                        "id": event.get("id"),
                                        "name": event.get("name"),
                                        "home_team": home_team,
                                        "away_team": away_team,
                                        "status": event.get("status", {}).get("type", {}).get("name", ""),
                                        "league": league_name,
                                        "date": event_date,
                                        "source": "ESPN"
                                    }
                                    
                                    all_matches.append(match_info)
                
                except Exception as e:
                    print(f"   ❌ Error fetching {league_name}: {e}")
        
        print(f"   Found {len(all_matches)} matches from ESPN")
        return all_matches
    
    async def search_thesportsdb(self, target_teams=None):
        """Search TheSportsDB for today's matches"""
        print("🏆 Searching TheSportsDB...")
        
        # Premier League, La Liga, Champions League
        league_ids = [4328, 4335, 4480]  # Premier League, La Liga, Champions League
        
        all_matches = []
        
        async with httpx.AsyncClient() as client:
            for league_id in league_ids:
                try:
                    # Get live scores
                    response = await client.get(f"https://www.thesportsdb.com/api/v1/json/3/livescore.php?l={league_id}")
                    
                    if response.status_code == 200:
                        data = response.json()
                        events = data.get("events", [])
                        
                        if events:
                            for event in events:
                                home_team = event.get("strHomeTeam", "")
                                away_team = event.get("strAwayTeam", "")
                                
                                # Filter for target teams if specified
                                if target_teams:
                                    found_target = False
                                    for target in target_teams:
                                        if (target.lower() in home_team.lower() or 
                                            target.lower() in away_team.lower()):
                                            found_target = True
                                            break
                                    
                                    if not found_target:
                                        continue
                                
                                match_info = {
                                    "id": event.get("idEvent"),
                                    "home_team": home_team,
                                    "away_team": away_team,
                                    "home_score": event.get("intHomeScore", 0),
                                    "away_score": event.get("intAwayScore", 0),
                                    "status": "LIVE",
                                    "league": event.get("strLeague", "Unknown"),
                                    "source": "TheSportsDB"
                                }
                                
                                all_matches.append(match_info)
                
                except Exception as e:
                    print(f"   ❌ Error fetching league {league_id}: {e}")
        
        print(f"   Found {len(all_matches)} matches from TheSportsDB")
        return all_matches

def convert_to_db_format(match_data, source="API"):
    """Convert API match data to database format"""
    
    if source == "football-data":
        home_team = match_data.get("homeTeam", {}).get("name", "Unknown")
        away_team = match_data.get("awayTeam", {}).get("name", "Unknown")
        
        # Map status
        status_map = {
            "LIVE": MatchStatus.LIVE,
            "IN_PLAY": MatchStatus.LIVE,
            "PAUSED": MatchStatus.LIVE,
            "FINISHED": MatchStatus.FINISHED,
            "SCHEDULED": MatchStatus.SCHEDULED,
            "TIMED": MatchStatus.SCHEDULED,
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
            "is_featured": True,  # Mark as featured for dashboard
            "stream_url": "https://demo.unified-streaming.com/k8s/features/stable/video/tears-of-steel/tears-of-steel.ism/.m3u8"  # Add test stream
        }
    
    elif source == "ESPN":
        return {
            "external_id": int(match_data.get("id", 0)),
            "title": f"{match_data['home_team']} vs {match_data['away_team']}",
            "home_team": match_data["home_team"],
            "away_team": match_data["away_team"],
            "home_score": 0,  # ESPN doesn't always provide scores in scoreboard
            "away_score": 0,
            "status": MatchStatus.LIVE if "IN_PROGRESS" in match_data.get("status", "") else MatchStatus.SCHEDULED,
            "scheduled_at": datetime.fromisoformat(match_data.get("date", "").replace("Z", "+00:00")) if match_data.get("date") else datetime.utcnow(),
            "is_featured": True,
            "stream_url": "https://demo.unified-streaming.com/k8s/features/stable/video/tears-of-steel/tears-of-steel.ism/.m3u8"
        }
    
    elif source == "TheSportsDB":
        return {
            "external_id": int(match_data.get("id", 0)),
            "title": f"{match_data['home_team']} vs {match_data['away_team']}",
            "home_team": match_data["home_team"],
            "away_team": match_data["away_team"],
            "home_score": int(match_data.get("home_score", 0)),
            "away_score": int(match_data.get("away_score", 0)),
            "status": MatchStatus.LIVE,
            "scheduled_at": datetime.utcnow(),
            "is_featured": True,
            "stream_url": "https://demo.unified-streaming.com/k8s/features/stable/video/tears-of-steel/tears-of-steel.ism/.m3u8"
        }

async def fetch_todays_matches():
    """Main function to fetch today's matches"""
    
    print("🔍 Searching for Today's Real Matches")
    print("=" * 50)
    
    # Target teams to look for
    target_teams = [
        "Real Madrid", "Madrid", 
        "Manchester City", "Man City", "City",
        "Barcelona", "Barca",
        "Liverpool", "Arsenal", "Chelsea",
        "Bayern Munich", "Bayern",
        "PSG", "Paris Saint-Germain"
    ]
    
    fetcher = ComprehensiveMatchFetcher()
    
    # Search all APIs
    football_data_matches = await fetcher.search_football_data_org(target_teams)
    espn_matches = await fetcher.search_espn_api(target_teams)
    thesportsdb_matches = await fetcher.search_thesportsdb(target_teams)
    
    # Combine all matches
    all_matches = []
    
    # Process Football-Data.org matches
    for match in football_data_matches:
        match_info = convert_to_db_format(match, "football-data")
        all_matches.append(match_info)
    
    # Process ESPN matches
    for match in espn_matches:
        match_info = convert_to_db_format(match, "ESPN")
        all_matches.append(match_info)
    
    # Process TheSportsDB matches
    for match in thesportsdb_matches:
        match_info = convert_to_db_format(match, "TheSportsDB")
        all_matches.append(match_info)
    
    print(f"\n📊 Total Matches Found: {len(all_matches)}")
    
    if not all_matches:
        print("⏰ No matches found for today with target teams")
        print("💡 This could mean:")
        print("   • No matches scheduled for today")
        print("   • Matches are at different times")
        print("   • API limitations")
        print("\n🔄 Try running during actual match hours for live data")
        return
    
    # Save to database
    db = SessionLocal()
    
    try:
        for match_info in all_matches:
            print(f"\n✅ Found: {match_info['title']}")
            print(f"   Status: {match_info['status']}")
            print(f"   Time: {match_info['scheduled_at']}")
            
            # Check if match already exists
            existing = db.query(Match).filter(
                Match.home_team == match_info["home_team"],
                Match.away_team == match_info["away_team"]
            ).first()
            
            if existing:
                # Update existing match
                for key, value in match_info.items():
                    if key != "external_id":
                        setattr(existing, key, value)
                print(f"   🔄 Updated existing match")
            else:
                # Create new match
                new_match = Match(**match_info)
                db.add(new_match)
                print(f"   ➕ Added new match")
        
        db.commit()
        
        # Show summary
        live_count = db.query(Match).filter(Match.status == MatchStatus.LIVE).count()
        featured_count = db.query(Match).filter(Match.featured == True).count()
        total_count = db.query(Match).count()
        
        print(f"\n📊 Database Summary:")
        print(f"   • Live matches: {live_count}")
        print(f"   • Featured matches: {featured_count}")
        print(f"   • Total matches: {total_count}")
        
        print(f"\n🎬 How to View Your Matches:")
        print(f"   1. Visit: http://localhost:3000/dashboard")
        print(f"   2. Click '🔴 Live' or 'All Leagues'")
        print(f"   3. Look for Real Madrid vs Manchester City!")
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Starting Today's Match Search")
    print(f"📅 Date: {date.today()}")
    print(f"🕘 Time: {datetime.now().strftime('%H:%M:%S')}")
    print()
    
    asyncio.run(fetch_todays_matches())