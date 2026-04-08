#!/usr/bin/env python3
"""
Fetch Real Matches from All Leagues
Gets live and upcoming matches from free APIs and displays them
"""
import asyncio
import httpx
import json
from datetime import datetime, date, timedelta

async def fetch_espn_matches():
    """Fetch matches from ESPN Soccer API (free, no key required)"""
    
    print("📺 Fetching from ESPN Soccer API...")
    
    leagues = [
        ("eng.1", "Premier League"),
        ("esp.1", "La Liga"), 
        ("ger.1", "Bundesliga"),
        ("ita.1", "Serie A"),
        ("fra.1", "Ligue 1"),
        ("uefa.champions", "Champions League"),
        ("uefa.europa", "Europa League"),
        ("conmebol.libertadores", "Copa Libertadores"),
        ("concacaf.champions", "CONCACAF Champions League"),
        ("fifa.world", "FIFA World Cup"),
        ("uefa.nations", "UEFA Nations League")
    ]
    
    all_matches = []
    
    async with httpx.AsyncClient() as client:
        for league_id, league_name in leagues:
            try:
                print(f"   Checking {league_name}...")
                response = await client.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{league_id}/scoreboard")
                
                if response.status_code == 200:
                    data = response.json()
                    events = data.get("events", [])
                    league_matches = 0
                    
                    for event in events:
                        # Get match status
                        status = event.get("status", {}).get("type", {}).get("name", "")
                        
                        # Check if match is today, tomorrow, or live
                        event_date = event.get("date", "")
                        is_relevant = False
                        scheduled_at = ""
                        
                        if event_date:
                            try:
                                match_datetime = datetime.fromisoformat(event_date.replace("Z", "+00:00"))
                                match_date = match_datetime.date()
                                today = date.today()
                                tomorrow = today + timedelta(days=1)
                                yesterday = today - timedelta(days=1)
                                
                                # Include matches from yesterday, today, and tomorrow
                                if match_date in [yesterday, today, tomorrow]:
                                    is_relevant = True
                                    scheduled_at = match_datetime.isoformat()
                            except:
                                pass
                        
                        # Always include live matches
                        if "IN_PROGRESS" in status or "HALFTIME" in status or "LIVE" in status:
                            is_relevant = True
                            if not scheduled_at:
                                scheduled_at = datetime.now().isoformat()
                        
                        if is_relevant:
                            # Get team names and scores
                            competitions = event.get("competitions", [{}])
                            if competitions:
                                competitors = competitions[0].get("competitors", [])
                                if len(competitors) >= 2:
                                    home_team = competitors[0].get("team", {}).get("displayName", "")
                                    away_team = competitors[1].get("team", {}).get("displayName", "")
                                    home_score = int(competitors[0].get("score", 0))
                                    away_score = int(competitors[1].get("score", 0))
                                    
                                    # Map status
                                    our_status = "scheduled"
                                    if "IN_PROGRESS" in status or "HALFTIME" in status or "LIVE" in status:
                                        our_status = "live"
                                    elif "FINAL" in status or "FINISHED" in status:
                                        our_status = "finished"
                                    
                                    match_info = {
                                        "id": int(event.get("id", 0)),
                                        "home_team": home_team,
                                        "away_team": away_team,
                                        "home_score": home_score,
                                        "away_score": away_score,
                                        "status": our_status,
                                        "scheduled_at": scheduled_at,
                                        "league": league_name,
                                        "source": "ESPN"
                                    }
                                    
                                    all_matches.append(match_info)
                                    league_matches += 1
                    
                    if league_matches > 0:
                        print(f"     Found {league_matches} matches")
            
            except Exception as e:
                print(f"   ❌ Error fetching {league_name}: {e}")
    
    print(f"   Total ESPN matches: {len(all_matches)}")
    return all_matches

async def fetch_thesportsdb_matches():
    """Fetch matches from TheSportsDB API (free, no key required)"""
    
    print("🏆 Fetching from TheSportsDB...")
    
    # Major league IDs
    leagues = [
        (4328, "Premier League"),
        (4335, "La Liga"),
        (4331, "Serie A"),
        (4332, "Bundesliga"),
        (4334, "Ligue 1"),
        (4480, "Champions League"),
        (4481, "Europa League")
    ]
    
    all_matches = []
    
    async with httpx.AsyncClient() as client:
        for league_id, league_name in leagues:
            try:
                print(f"   Checking {league_name}...")
                
                # Get live scores
                response = await client.get(f"https://www.thesportsdb.com/api/v1/json/3/livescore.php?l={league_id}")
                
                if response.status_code == 200:
                    data = response.json()
                    events = data.get("events", [])
                    
                    if events:
                        for event in events:
                            home_team = event.get("strHomeTeam", "")
                            away_team = event.get("strAwayTeam", "")
                            
                            if home_team and away_team:
                                match_info = {
                                    "id": int(event.get("idEvent", 0)),
                                    "home_team": home_team,
                                    "away_team": away_team,
                                    "home_score": int(event.get("intHomeScore", 0)),
                                    "away_score": int(event.get("intAwayScore", 0)),
                                    "status": "live",
                                    "scheduled_at": datetime.now().isoformat(),
                                    "league": league_name,
                                    "source": "TheSportsDB"
                                }
                                
                                all_matches.append(match_info)
                        
                        print(f"     Found {len(events)} live matches")
            
            except Exception as e:
                print(f"   ❌ Error fetching {league_name}: {e}")
    
    print(f"   Total TheSportsDB matches: {len(all_matches)}")
    return all_matches

async def fetch_api_football():
    """Fetch from API-Football (free tier available)"""
    
    # You can get a free API key from https://www.api-football.com/
    api_key = "YOUR_API_KEY_HERE"  # Replace with actual key
    
    if api_key == "YOUR_API_KEY_HERE":
        print("⚠️  API-Football key not configured, skipping...")
        return []
    
    print("⚽ Fetching from API-Football...")
    
    matches = []
    
    async with httpx.AsyncClient() as client:
        try:
            # Get today's fixtures
            today = date.today().isoformat()
            
            response = await client.get(
                "https://v3.football.api-sports.io/fixtures",
                headers={"x-apisports-key": api_key},
                params={"date": today}
            )
            
            if response.status_code == 200:
                data = response.json()
                fixtures = data.get("response", [])
                
                for fixture in fixtures:
                    fixture_data = fixture.get("fixture", {})
                    teams = fixture.get("teams", {})
                    goals = fixture.get("goals", {})
                    league = fixture.get("league", {})
                    
                    home_team = teams.get("home", {}).get("name", "")
                    away_team = teams.get("away", {}).get("name", "")
                    
                    # Map status
                    status_map = {
                        "1H": "live", "HT": "live", "2H": "live", "ET": "live", "P": "live",
                        "FT": "finished", "AET": "finished", "PEN": "finished",
                        "TBD": "scheduled", "NS": "scheduled", "PST": "scheduled"
                    }
                    
                    api_status = fixture_data.get("status", {}).get("short", "NS")
                    our_status = status_map.get(api_status, "scheduled")
                    
                    match_info = {
                        "id": fixture_data.get("id", 0),
                        "home_team": home_team,
                        "away_team": away_team,
                        "home_score": goals.get("home", 0) or 0,
                        "away_score": goals.get("away", 0) or 0,
                        "status": our_status,
                        "scheduled_at": fixture_data.get("date", ""),
                        "league": league.get("name", "Unknown League"),
                        "source": "API-Football"
                    }
                    
                    matches.append(match_info)
                
                print(f"   Found {len(matches)} matches from API-Football")
            else:
                print(f"   ❌ API Error: {response.status_code}")
        
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return matches

def display_matches(matches):
    """Display matches in a nice format"""
    
    if not matches:
        print("❌ No matches found!")
        return
    
    # Group by status
    live_matches = [m for m in matches if m["status"] == "live"]
    upcoming_matches = [m for m in matches if m["status"] == "scheduled"]
    finished_matches = [m for m in matches if m["status"] == "finished"]
    
    print(f"\n📊 Match Summary:")
    print(f"   🔴 Live matches: {len(live_matches)}")
    print(f"   ⏰ Upcoming matches: {len(upcoming_matches)}")
    print(f"   ✅ Finished matches: {len(finished_matches)}")
    
    # Show live matches
    if live_matches:
        print(f"\n🔴 LIVE MATCHES:")
        print("-" * 70)
        for match in live_matches[:10]:  # Show first 10
            print(f"⚽ {match['home_team']} {match['home_score']}-{match['away_score']} {match['away_team']}")
            print(f"   📺 {match['league']} | Source: {match['source']}")
            print()
    
    # Show upcoming matches
    if upcoming_matches:
        print(f"\n⏰ UPCOMING MATCHES:")
        print("-" * 70)
        for match in upcoming_matches[:15]:  # Show first 15
            try:
                scheduled_time = datetime.fromisoformat(match['scheduled_at'].replace('Z', '+00:00'))
                time_str = scheduled_time.strftime('%H:%M')
            except:
                time_str = "TBD"
            
            print(f"🕐 {match['home_team']} vs {match['away_team']} at {time_str}")
            print(f"   📺 {match['league']} | Source: {match['source']}")
            print()
    
    # Show recent finished matches
    if finished_matches:
        print(f"\n✅ RECENT FINISHED MATCHES:")
        print("-" * 70)
        for match in finished_matches[:10]:  # Show first 10
            print(f"⚽ {match['home_team']} {match['home_score']}-{match['away_score']} {match['away_team']}")
            print(f"   📺 {match['league']} | Source: {match['source']}")
            print()

def save_matches_summary(matches):
    """Save matches to a JSON file for later use"""
    
    try:
        with open('real_matches_data.json', 'w') as f:
            json.dump(matches, f, indent=2, default=str)
        
        print(f"💾 Saved {len(matches)} matches to 'real_matches_data.json'")
        print("   You can use this data to populate your database!")
        
    except Exception as e:
        print(f"❌ Error saving matches: {e}")

async def main():
    """Main function to fetch all matches"""
    
    print("🔍 Fetching Real Live and Upcoming Matches")
    print("=" * 60)
    print(f"📅 Date: {date.today()}")
    print(f"🕘 Time: {datetime.now().strftime('%H:%M:%S')}")
    print()
    
    # Fetch from all sources
    espn_matches = await fetch_espn_matches()
    thesportsdb_matches = await fetch_thesportsdb_matches()
    api_football_matches = await fetch_api_football()
    
    # Combine all matches
    all_matches = espn_matches + thesportsdb_matches + api_football_matches
    
    # Remove duplicates based on team names
    unique_matches = []
    seen_matches = set()
    
    for match in all_matches:
        match_key = f"{match['home_team'].lower()}_{match['away_team'].lower()}"
        if match_key not in seen_matches:
            seen_matches.add(match_key)
            unique_matches.append(match)
    
    print(f"\n🎯 Total unique matches found: {len(unique_matches)}")
    
    # Display matches
    display_matches(unique_matches)
    
    # Save to file
    save_matches_summary(unique_matches)
    
    print(f"\n🎬 Next Steps:")
    print(f"   1. These are REAL matches from live APIs")
    print(f"   2. You can use this data to populate your database")
    print(f"   3. Run this script regularly to get fresh match data")
    print(f"   4. For more matches, get free API keys from:")
    print(f"      • Football-Data.org: https://www.football-data.org/client/register")
    print(f"      • API-Football: https://www.api-football.com/")
    
    return unique_matches

if __name__ == "__main__":
    matches = asyncio.run(main())
    
    if matches:
        print(f"\n🎉 Successfully fetched {len(matches)} real matches!")
        print(f"   Live matches: {len([m for m in matches if m['status'] == 'live'])}")
        print(f"   Upcoming matches: {len([m for m in matches if m['status'] == 'scheduled'])}")
    else:
        print(f"\n💡 No matches found. This could mean:")
        print(f"   • No matches scheduled for today")
        print(f"   • Try again during European match hours (12:00-22:00 UTC)")
        print(f"   • Get free API keys for more comprehensive data")