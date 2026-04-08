#!/usr/bin/env python3
"""
Simple TheSportsDB API Test
Test the actual endpoints to find correct league IDs
"""
import asyncio
import httpx

async def test_thesportsdb():
    """Test TheSportsDB V1 API endpoints"""
    print("🔌 Testing TheSportsDB V1 API (Free, No Key Required)...")
    
    base_url = "https://www.thesportsdb.com/api/v1/json/1"  # V1 API
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        
        # Test 1: Search for Premier League
        print("\n📋 Test 1: Searching for Premier League...")
        try:
            response = await client.get(f"{base_url}/search_all_leagues.php?c=England")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Response received: {response.status_code}")
                
                if "countrys" in data and data["countrys"]:
                    print(f"Found {len(data['countrys'])} leagues in England:")
                    for league in data["countrys"][:5]:  # Show first 5
                        league_name = league.get("strLeague", "Unknown")
                        league_id = league.get("idLeague", "Unknown")
                        print(f"   {league_name} (ID: {league_id})")
                else:
                    print("No leagues found in response")
            else:
                print(f"❌ Error: {response.status_code}")
        except Exception as e:
            print(f"❌ Exception: {e}")
        
        # Test 2: Try a different approach - search for specific team
        print("\n🔍 Test 2: Searching for Arsenal...")
        try:
            response = await client.get(f"{base_url}/searchteams.php?t=Arsenal")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Response received: {response.status_code}")
                
                if "teams" in data and data["teams"]:
                    team = data["teams"][0]
                    team_name = team.get("strTeam", "Unknown")
                    team_id = team.get("idTeam", "Unknown")
                    league = team.get("strLeague", "Unknown")
                    print(f"   Team: {team_name} (ID: {team_id})")
                    print(f"   League: {league}")
                else:
                    print("No teams found")
            else:
                print(f"❌ Error: {response.status_code}")
        except Exception as e:
            print(f"❌ Exception: {e}")
        
        # Test 3: Try to get events for a known team
        print("\n⚽ Test 3: Getting Arsenal fixtures...")
        try:
            # First get Arsenal's team ID
            response = await client.get(f"{base_url}/searchteams.php?t=Arsenal")
            if response.status_code == 200:
                data = response.json()
                if "teams" in data and data["teams"]:
                    team_id = data["teams"][0].get("idTeam")
                    print(f"   Arsenal Team ID: {team_id}")
                    
                    # Now get their fixtures
                    fixtures_response = await client.get(f"{base_url}/eventsnext.php?id={team_id}")
                    if fixtures_response.status_code == 200:
                        fixtures_data = fixtures_response.json()
                        print(f"✅ Fixtures response: {fixtures_response.status_code}")
                        
                        if "events" in fixtures_data and fixtures_data["events"]:
                            print(f"Found {len(fixtures_data['events'])} upcoming fixtures:")
                            for i, event in enumerate(fixtures_data["events"][:3]):
                                home_team = event.get("strHomeTeam", "Unknown")
                                away_team = event.get("strAwayTeam", "Unknown")
                                date = event.get("dateEvent", "Unknown")
                                time = event.get("strTime", "Unknown")
                                print(f"   {i+1}. {home_team} vs {away_team} - {date} {time}")
                        else:
                            print("No fixtures found")
                    else:
                        print(f"❌ Fixtures error: {fixtures_response.status_code}")
        except Exception as e:
            print(f"❌ Exception: {e}")
        
        # Test 4: Try latest scores
        print("\n🔴 Test 4: Getting latest scores...")
        try:
            response = await client.get(f"{base_url}/latestscore.php")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Latest scores response: {response.status_code}")
                
                if "events" in data and data["events"]:
                    print(f"Found {len(data['events'])} recent matches:")
                    for i, event in enumerate(data["events"][:3]):
                        home_team = event.get("strHomeTeam", "Unknown")
                        away_team = event.get("strAwayTeam", "Unknown")
                        home_score = event.get("intHomeScore", "?")
                        away_score = event.get("intAwayScore", "?")
                        date = event.get("dateEvent", "Unknown")
                        print(f"   {i+1}. {home_team} {home_score} - {away_score} {away_team} ({date})")
                else:
                    print("No recent matches found")
            else:
                print(f"❌ Error: {response.status_code}")
        except Exception as e:
            print(f"❌ Exception: {e}")

if __name__ == "__main__":
    asyncio.run(test_thesportsdb())