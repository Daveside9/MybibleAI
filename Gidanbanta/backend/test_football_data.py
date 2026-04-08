#!/usr/bin/env python3
"""
Test Football-Data.org API
Free API with good coverage of major leagues
"""
import asyncio
import sys
import os
from datetime import datetime, timedelta

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.football_data_api import FootballDataClient, FOOTBALL_DATA_COMPETITIONS

async def test_football_data_api():
    """Test Football-Data.org API"""
    print("🔌 Testing Football-Data.org API (Free Tier)...")
    print("📝 Note: This API has 10 requests/minute limit on free tier")
    
    async with FootballDataClient() as client:  # No API key needed for basic access
        
        # Test 1: Get available competitions
        print("\n📋 Test 1: Getting available competitions...")
        try:
            competitions = await client.get_competitions()
            
            if competitions:
                print(f"✅ Found {len(competitions)} competitions")
                
                # Show major competitions
                print("\n🏆 Major competitions available:")
                for comp in competitions:
                    comp_name = comp.get("name", "Unknown")
                    comp_code = comp.get("code", "Unknown")
                    area = comp.get("area", {}).get("name", "Unknown")
                    
                    # Filter for major leagues
                    if any(major in comp_name for major in ["Premier League", "La Liga", "Serie A", "Bundesliga", "Champions League"]):
                        print(f"   {comp_name} ({comp_code}) - {area}")
            else:
                print("❌ No competitions found")
                return False
                
        except Exception as e:
            print(f"❌ Exception: {e}")
            return False
        
        # Small delay to respect rate limits
        await asyncio.sleep(6)  # 10 requests/minute = 6 seconds between requests
        
        # Test 2: Get today's matches
        print("\n📅 Test 2: Getting today's matches...")
        try:
            todays_matches = await client.get_todays_matches()
            
            if todays_matches:
                print(f"✅ Found {len(todays_matches)} matches today")
                
                # Show first few matches
                for i, match in enumerate(todays_matches[:3]):
                    home_team = match.get("homeTeam", {}).get("name", "Unknown")
                    away_team = match.get("awayTeam", {}).get("name", "Unknown")
                    competition = match.get("competition", {}).get("name", "Unknown")
                    utc_date = match.get("utcDate", "Unknown")
                    status = match.get("status", "Unknown")
                    
                    print(f"   {i+1}. {home_team} vs {away_team} ({competition}) - {utc_date} [{status}]")
            else:
                print("ℹ️  No matches today (this is normal)")
                
        except Exception as e:
            print(f"❌ Exception: {e}")
        
        # Small delay
        await asyncio.sleep(6)
        
        # Test 3: Get Premier League matches
        print("\n⚽ Test 3: Getting Premier League matches...")
        try:
            # Get matches for next 7 days
            today = datetime.now().date()
            end_date = today + timedelta(days=7)
            
            pl_matches = await client.get_competition_matches(
                "PL",  # Premier League code
                date_from=str(today),
                date_to=str(end_date)
            )
            
            if pl_matches:
                print(f"✅ Found {len(pl_matches)} Premier League matches in next 7 days")
                
                for i, match in enumerate(pl_matches[:5]):
                    home_team = match.get("homeTeam", {}).get("name", "Unknown")
                    away_team = match.get("awayTeam", {}).get("name", "Unknown")
                    utc_date = match.get("utcDate", "Unknown")
                    status = match.get("status", "Unknown")
                    
                    # Parse date for better display
                    try:
                        dt = datetime.fromisoformat(utc_date.replace("Z", "+00:00"))
                        formatted_date = dt.strftime("%Y-%m-%d %H:%M")
                    except:
                        formatted_date = utc_date
                    
                    print(f"   {i+1}. {home_team} vs {away_team} - {formatted_date} [{status}]")
            else:
                print("ℹ️  No Premier League matches in next 7 days")
                
        except Exception as e:
            print(f"❌ Exception: {e}")
        
        print(f"\n✅ Football-Data.org API is working!")
        print(f"📊 Available competitions: {list(FOOTBALL_DATA_COMPETITIONS.keys())}")
        return True

async def main():
    """Main function"""
    print("🚀 Football-Data.org API Test")
    print("=" * 50)
    
    success = await test_football_data_api()
    
    if success:
        print(f"\n🎉 API test successful!")
        print(f"💡 This API provides real match data for:")
        for league_name, code in FOOTBALL_DATA_COMPETITIONS.items():
            print(f"   • {league_name} ({code})")
        print(f"\n📝 Note: Free tier has 10 requests/minute limit")
        print(f"🔄 You can now sync real match data!")
    else:
        print(f"\n❌ API test failed")

if __name__ == "__main__":
    asyncio.run(main())