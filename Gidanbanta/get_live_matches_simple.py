#!/usr/bin/env python3
"""
Simple Live Match Fetcher - No Database Dependencies
Just fetches and displays real live match data from free APIs
"""
import asyncio
import httpx
import json
from datetime import datetime, date

async def get_espn_live_matches():
    """Get live matches from ESPN Soccer API (free, no key required)"""
    print("📺 Fetching live matches from ESPN Soccer API...")
    
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
                print(f"   Checking {league_name}...")
                response = await client.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{league_id}/scoreboard")
                
                if response.status_code == 200:
                    data = response.json()
                    events = data.get("events", [])
                    
                    for event in events:
                        # Get match status
                        status = event.get("status", {}).get("type", {}).get("name", "")
                        
                        # Check if match is today or live
                        event_date = event.get("date", "")
                        is_today = False
                        if event_date:
                            try:
                                match_date = datetime.fromisoformat(event_date.replace("Z", "+00:00")).date()
                                is_today = match_date == date.today()
                            except:
                                pass
                        
                        # Only include live matches or today's matches
                        if "IN_PROGRESS" in status or "HALFTIME" in status or is_today:
                            # Get team names
                            competitions = event.get("competitions", [{}])
                            if competitions:
                                competitors = competitions[0].get("competitors", [])
                                if len(competitors) >= 2:
                                    home_team = competitors[0].get("team", {}).get("displayName", "")
                                    away_team = competitors[1].get("team", {}).get("displayName", "")
                                    home_score = competitors[0].get("score", "0")
                                    away_score = competitors[1].get("score", "0")
                                    
                                    match_info = {
                                        "id": event.get("id"),
                                        "name": event.get("name"),
                                        "home_team": home_team,
                                        "away_team": away_team,
                                        "home_score": home_score,
                                        "away_score": away_score,
                                        "status": status,
                                        "league": league_name,
                                        "date": event_date,
                                        "is_live": "IN_PROGRESS" in status or "HALFTIME" in status,
                                        "source": "ESPN"
                                    }
                                    
                                    all_matches.append(match_info)
            
            except Exception as e:
                print(f"   ❌ Error fetching {league_name}: {e}")
    
    return all_matches

async def get_thesportsdb_live_matches():
    """Get live matches from TheSportsDB (free, no key required)"""
    print("🏆 Fetching live matches from TheSportsDB...")
    
    # Premier League, La Liga, Champions League, Serie A, Bundesliga
    league_configs = [
        (4328, "Premier League"),
        (4335, "La Liga"),
        (4480, "Champions League"),
        (4331, "Serie A"),
        (4331, "Bundesliga")
    ]
    
    all_matches = []
    
    async with httpx.AsyncClient() as client:
        for league_id, league_name in league_configs:
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
                            
                            match_info = {
                                "id": event.get("idEvent"),
                                "home_team": home_team,
                                "away_team": away_team,
                                "home_score": event.get("intHomeScore", "0"),
                                "away_score": event.get("intAwayScore", "0"),
                                "status": "LIVE",
                                "league": league_name,
                                "is_live": True,
                                "source": "TheSportsDB"
                            }
                            
                            all_matches.append(match_info)
            
            except Exception as e:
                print(f"   ❌ Error fetching {league_name}: {e}")
    
    return all_matches

def filter_target_teams(matches, target_teams):
    """Filter matches for specific teams"""
    filtered = []
    
    for match in matches:
        home_team = match.get("home_team", "").lower()
        away_team = match.get("away_team", "").lower()
        
        for target in target_teams:
            if target.lower() in home_team or target.lower() in away_team:
                filtered.append(match)
                break
    
    return filtered

async def main():
    """Main function to fetch and display live matches"""
    
    print("🔍 Fetching Real Live Match Data")
    print("=" * 50)
    print(f"📅 Date: {date.today()}")
    print(f"🕘 Time: {datetime.now().strftime('%H:%M:%S')}")
    print()
    
    # Target teams to look for
    target_teams = [
        "Real Madrid", "Madrid", 
        "Manchester City", "Man City", "City",
        "Barcelona", "Barca",
        "Liverpool", "Arsenal", "Chelsea",
        "Bayern Munich", "Bayern",
        "PSG", "Paris Saint-Germain",
        "Manchester United", "Man United"
    ]
    
    # Fetch from all sources
    espn_matches = await get_espn_live_matches()
    thesportsdb_matches = await get_thesportsdb_live_matches()
    
    # Combine all matches
    all_matches = espn_matches + thesportsdb_matches
    
    print(f"\n📊 Total Matches Found: {len(all_matches)}")
    
    if not all_matches:
        print("⏰ No live matches found right now")
        print("💡 This could mean:")
        print("   • No matches are currently live")
        print("   • Matches are scheduled for later today")
        print("   • Try again during European match hours (12:00-22:00 UTC)")
        return
    
    # Show all matches
    print(f"\n🔴 All Matches Found:")
    print("-" * 60)
    
    live_matches = []
    scheduled_matches = []
    
    for match in all_matches:
        is_live = match.get("is_live", False)
        
        if is_live:
            live_matches.append(match)
        else:
            scheduled_matches.append(match)
        
        status_icon = "🔴" if is_live else "⏰"
        print(f"{status_icon} {match.get('home_team', 'Unknown')} vs {match.get('away_team', 'Unknown')}")
        print(f"   Score: {match.get('home_score', '0')} - {match.get('away_score', '0')}")
        print(f"   League: {match.get('league', 'Unknown')}")
        print(f"   Status: {match.get('status', 'Unknown')}")
        print(f"   Source: {match.get('source', 'Unknown')}")
        print()
    
    # Filter for target teams
    target_matches = filter_target_teams(all_matches, target_teams)
    
    if target_matches:
        print(f"⭐ Matches with Target Teams ({len(target_matches)}):")
        print("-" * 60)
        
        for match in target_matches:
            is_live = match.get("is_live", False)
            status_icon = "🔴" if is_live else "⏰"
            print(f"{status_icon} {match.get('home_team', 'Unknown')} vs {match.get('away_team', 'Unknown')}")
            print(f"   Score: {match.get('home_score', '0')} - {match.get('away_score', '0')}")
            print(f"   League: {match.get('league', 'Unknown')}")
            print(f"   Status: {match.get('status', 'Unknown')}")
            print()
    
    # Summary
    print(f"📊 Summary:")
    print(f"   • Live matches: {len(live_matches)}")
    print(f"   • Scheduled today: {len(scheduled_matches)}")
    print(f"   • Target team matches: {len(target_matches)}")
    
    # Check for Real Madrid vs Manchester City specifically
    real_madrid_city = None
    for match in all_matches:
        home = match.get("home_team", "").lower()
        away = match.get("away_team", "").lower()
        
        if (("real madrid" in home or "madrid" in home) and ("manchester city" in away or "city" in away)) or \
           (("real madrid" in away or "madrid" in away) and ("manchester city" in home or "city" in home)):
            real_madrid_city = match
            break
    
    if real_madrid_city:
        print(f"\n⚽ FOUND: Real Madrid vs Manchester City!")
        print(f"   Status: {real_madrid_city.get('status', 'Unknown')}")
        print(f"   Score: {real_madrid_city.get('home_score', '0')} - {real_madrid_city.get('away_score', '0')}")
        print(f"   League: {real_madrid_city.get('league', 'Unknown')}")
        if real_madrid_city.get("is_live"):
            print(f"   🔴 LIVE NOW!")
        else:
            print(f"   ⏰ Scheduled for today")
    else:
        print(f"\n⚽ Real Madrid vs Manchester City not found in today's matches")
        print(f"   This match might be:")
        print(f"   • Scheduled for a different date")
        print(f"   • Not covered by these free APIs")
        print(f"   • Using different team name variations")
    
    print(f"\n🎬 Next Steps:")
    print(f"   1. Use the Real Madrid vs City match script to add it manually")
    print(f"   2. Visit your dashboard to see live matches")
    print(f"   3. Try again during actual match hours for live data")

if __name__ == "__main__":
    asyncio.run(main())