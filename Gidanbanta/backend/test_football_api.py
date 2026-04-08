#!/usr/bin/env python3
"""
Test Football API Connection
Verifies that the RapidAPI Football API is working correctly
"""
import asyncio
import sys
import os
from datetime import datetime, timedelta

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.football_api import FootballAPIClient
from app.core.config import settings

async def test_api_connection():
    """Test basic API connection"""
    print("🔌 Testing Football API connection...")
    print(f"🔑 API Key: {settings.FOOTBALL_API_KEY[:20]}...")
    print(f"🌐 Base URL: {settings.FOOTBALL_API_BASE_URL}")
    
    async with FootballAPIClient(
        api_key=settings.FOOTBALL_API_KEY,
        base_url=settings.FOOTBALL_API_BASE_URL,
        rapidapi_host=settings.RAPIDAPI_HOST
    ) as client:
        
        # Test 1: Get leagues
        print("\n📋 Test 1: Fetching available leagues...")
        leagues = await client.get_leagues(season=2024)
        
        if leagues:
            print(f"✅ Found {len(leagues)} leagues for 2024 season")
            
            # Show major leagues
            major_leagues = ["Premier League", "La Liga", "Serie A", "Champions League", "Europa League"]
            print("\n🏆 Major leagues found:")
            for league_data in leagues[:20]:  # Show first 20
                league_name = league_data.get("league", {}).get("name", "Unknown")
                league_id = league_data.get("league", {}).get("id", "Unknown")
                if any(major in league_name for major in major_leagues):
                    print(f"   {league_name} (ID: {league_id})")
        else:
            print("❌ Failed to fetch leagues")
            return False
        
        # Test 2: Get fixtures for today
        print("\n📅 Test 2: Fetching today's fixtures...")
        today = datetime.now().date()
        fixtures = await client.get_fixtures(
            date_from=str(today),
            date_to=str(today)
        )
        
        if fixtures is not None:
            print(f"✅ Found {len(fixtures)} fixtures for today")
            
            # Show sample fixtures
            for i, fixture in enumerate(fixtures[:5]):  # Show first 5
                fixture_info = fixture.get("fixture", {})
                teams = fixture.get("teams", {})
                league = fixture.get("league", {})
                
                home_team = teams.get("home", {}).get("name", "Unknown")
                away_team = teams.get("away", {}).get("name", "Unknown")
                league_name = league.get("name", "Unknown")
                match_time = fixture_info.get("date", "Unknown")
                
                print(f"   {i+1}. {home_team} vs {away_team} ({league_name}) at {match_time}")
        else:
            print("❌ Failed to fetch fixtures")
            return False
        
        # Test 3: Get live fixtures
        print("\n🔴 Test 3: Fetching live fixtures...")
        live_fixtures = await client.get_live_fixtures()
        
        if live_fixtures is not None:
            print(f"✅ Found {len(live_fixtures)} live fixtures")
            
            # Show live fixtures
            for i, fixture in enumerate(live_fixtures[:3]):  # Show first 3
                fixture_info = fixture.get("fixture", {})
                teams = fixture.get("teams", {})
                goals = fixture.get("goals", {})
                
                home_team = teams.get("home", {}).get("name", "Unknown")
                away_team = teams.get("away", {}).get("name", "Unknown")
                home_score = goals.get("home", 0)
                away_score = goals.get("away", 0)
                status = fixture_info.get("status", {}).get("short", "Unknown")
                
                print(f"   {i+1}. {home_team} {home_score} - {away_score} {away_team} ({status})")
        else:
            print("❌ Failed to fetch live fixtures")
            return False
        
        print("\n✅ All API tests passed! Your Football API is working correctly.")
        return True

async def test_specific_league():
    """Test fetching fixtures for a specific league"""
    print("\n🏆 Testing Premier League fixtures...")
    
    async with FootballAPIClient(
        api_key=settings.FOOTBALL_API_KEY,
        base_url=settings.FOOTBALL_API_BASE_URL,
        rapidapi_host=settings.RAPIDAPI_HOST
    ) as client:
        
        # Premier League ID is 39
        today = datetime.now().date()
        end_date = today + timedelta(days=7)
        
        fixtures = await client.get_fixtures(
            date_from=str(today),
            date_to=str(end_date),
            league_id=39  # Premier League
        )
        
        if fixtures:
            print(f"✅ Found {len(fixtures)} Premier League fixtures in the next 7 days")
            
            for i, fixture in enumerate(fixtures[:10]):  # Show first 10
                fixture_info = fixture.get("fixture", {})
                teams = fixture.get("teams", {})
                
                home_team = teams.get("home", {}).get("name", "Unknown")
                away_team = teams.get("away", {}).get("name", "Unknown")
                match_date = fixture_info.get("date", "Unknown")
                status = fixture_info.get("status", {}).get("short", "Unknown")
                
                # Parse date for better display
                try:
                    dt = datetime.fromisoformat(match_date.replace("Z", "+00:00"))
                    formatted_date = dt.strftime("%Y-%m-%d %H:%M")
                except:
                    formatted_date = match_date
                
                print(f"   {i+1}. {home_team} vs {away_team} - {formatted_date} ({status})")
        else:
            print("❌ No Premier League fixtures found")

async def main():
    """Main function"""
    print("🚀 Football API Test Suite")
    print("=" * 50)
    
    # Test basic connection
    success = await test_api_connection()
    
    if success:
        # Test specific league
        await test_specific_league()
        
        print("\n🎉 All tests completed successfully!")
        print("You can now run 'python sync_real_matches.py' to sync real match data.")
    else:
        print("\n❌ API tests failed. Please check your API key and connection.")

if __name__ == "__main__":
    asyncio.run(main())