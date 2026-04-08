#!/usr/bin/env python3
"""
Check what live matches are available right now
"""
import asyncio
import httpx
from datetime import datetime

async def check_live_matches_now():
    """Check all free APIs for live matches right now"""
    
    print("🔍 Checking Live Matches Right Now")
    print("=" * 50)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print()
    
    total_live = 0
    
    # 1. ESPN Soccer API
    print("📺 ESPN Soccer API:")
    leagues = {
        "eng.1": "Premier League",
        "esp.1": "La Liga", 
        "ger.1": "Bundesliga",
        "ita.1": "Serie A",
        "fra.1": "Ligue 1"
    }
    
    espn_live = 0
    async with httpx.AsyncClient() as client:
        for league_id, league_name in leagues.items():
            try:
                response = await client.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{league_id}/scoreboard")
                if response.status_code == 200:
                    data = response.json()
                    league_live = 0
                    for event in data.get("events", []):
                        status = event.get("status", {}).get("type", {}).get("name", "")
                        if "IN_PROGRESS" in status or "HALFTIME" in status:
                            league_live += 1
                            espn_live += 1
                            print(f"   🔴 {event.get('name', 'Unknown Match')} ({status})")
                    
                    if league_live == 0:
                        print(f"   ⚪ {league_name}: No live matches")
                else:
                    print(f"   ❌ {league_name}: API Error ({response.status_code})")
            except Exception as e:
                print(f"   ❌ {league_name}: Connection Error")
    
    total_live += espn_live
    print(f"   📊 ESPN Total: {espn_live} live matches")
    print()
    
    # 2. TheSportsDB
    print("🏆 TheSportsDB API:")
    thesportsdb_live = 0
    async with httpx.AsyncClient() as client:
        try:
            # Check Premier League live scores
            response = await client.get("https://www.thesportsdb.com/api/v1/json/3/livescore.php?l=4328")
            if response.status_code == 200:
                data = response.json()
                if data.get("events"):
                    for event in data["events"]:
                        thesportsdb_live += 1
                        home = event.get("strHomeTeam", "Unknown")
                        away = event.get("strAwayTeam", "Unknown")
                        score = f"{event.get('intHomeScore', 0)}-{event.get('intAwayScore', 0)}"
                        print(f"   🔴 {home} vs {away} ({score})")
                else:
                    print("   ⚪ Premier League: No live matches")
            else:
                print(f"   ❌ API Error ({response.status_code})")
        except Exception as e:
            print(f"   ❌ Connection Error: {e}")
    
    total_live += thesportsdb_live
    print(f"   📊 TheSportsDB Total: {thesportsdb_live} live matches")
    print()
    
    # 3. Summary
    print("📊 SUMMARY")
    print("-" * 30)
    if total_live > 0:
        print(f"🔴 Found {total_live} live matches!")
        print("✅ You can use these for real live streaming")
        print()
        print("🚀 To update your database:")
        print("   cd Gidanbanta/backend")
        print("   python setup_real_live_matches.py")
    else:
        print("⏰ No live matches found right now")
        print()
        print("🕒 Best times to find live matches (UTC):")
        print("   • Saturday 12:00-18:00 (Premier League)")
        print("   • Sunday 13:00-20:00 (La Liga, Serie A)")
        print("   • Tuesday/Wednesday 19:00-22:00 (Champions League)")
        print("   • Thursday 17:00-22:00 (Europa League)")
        print()
        print("💡 For testing, you can use the existing test matches:")
        print("   Visit: http://localhost:3000/match/1")

if __name__ == "__main__":
    asyncio.run(check_live_matches_now())