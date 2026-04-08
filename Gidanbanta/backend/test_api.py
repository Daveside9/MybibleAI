"""
Quick test script to verify RapidAPI Football API connection
"""
import asyncio
from app.services.football_api import FootballAPIClient
from app.core.config import settings
from datetime import datetime

async def test_api():
    print("Testing RapidAPI Football API connection...")
    print(f"API Key: {settings.FOOTBALL_API_KEY[:20]}...")
    print(f"Base URL: {settings.FOOTBALL_API_BASE_URL}")
    print(f"RapidAPI Host: {settings.RAPIDAPI_HOST}")
    print()
    
    async with FootballAPIClient(
        api_key=settings.FOOTBALL_API_KEY,
        base_url=settings.FOOTBALL_API_BASE_URL,
        rapidapi_host=settings.RAPIDAPI_HOST
    ) as client:
        # Test 1: Get today's fixtures
        today = datetime.now().strftime("%Y-%m-%d")
        print(f"Fetching fixtures for {today}...")
        
        fixtures = await client.get_fixtures(date_from=today, date_to=today)
        
        if fixtures:
            print(f"✅ Success! Found {len(fixtures)} fixtures")
            if len(fixtures) > 0:
                print("\nSample match:")
                match = fixtures[0]
                print(f"  {match['teams']['home']['name']} vs {match['teams']['away']['name']}")
                print(f"  League: {match['league']['name']}")
                print(f"  Status: {match['fixture']['status']['short']}")
        else:
            print("❌ No fixtures returned or API error")
            print("This might be normal if there are no matches today")
            print("Try checking your RapidAPI dashboard for quota/limits")

if __name__ == "__main__":
    asyncio.run(test_api())
