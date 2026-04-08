#!/usr/bin/env python3
"""
Sync Real Football Matches from TheSportsDB
Free API for real match data from major leagues
"""
import asyncio
import sys
import os
from datetime import datetime

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import get_db
from app.services.thesportsdb_service import TheSportsDBService
from app.services.thesportsdb_api import TheSportsDBClient, THESPORTSDB_LEAGUES

async def test_api_connection():
    """Test TheSportsDB API connection"""
    print("🔌 Testing TheSportsDB API connection...")
    
    async with TheSportsDBClient() as client:
        
        # Test 1: Get Premier League fixtures
        print("\n📋 Test 1: Fetching Premier League fixtures...")
        fixtures = await client.get_next_fixtures("4328", count=5)  # Premier League ID
        
        if fixtures:
            print(f"✅ Found {len(fixtures)} upcoming Premier League fixtures")
            
            for i, fixture in enumerate(fixtures[:3]):
                home_team = fixture.get("strHomeTeam", "Unknown")
                away_team = fixture.get("strAwayTeam", "Unknown")
                match_date = fixture.get("dateEvent", "Unknown")
                match_time = fixture.get("strTime", "Unknown")
                
                print(f"   {i+1}. {home_team} vs {away_team} - {match_date} {match_time}")
        else:
            print("❌ No Premier League fixtures found")
            return False
        
        # Test 2: Get recent results
        print("\n📊 Test 2: Fetching recent Premier League results...")
        past_fixtures = await client.get_last_fixtures("4328", count=3)
        
        if past_fixtures:
            print(f"✅ Found {len(past_fixtures)} recent Premier League results")
            
            for i, fixture in enumerate(past_fixtures[:3]):
                home_team = fixture.get("strHomeTeam", "Unknown")
                away_team = fixture.get("strAwayTeam", "Unknown")
                home_score = fixture.get("intHomeScore", "?")
                away_score = fixture.get("intAwayScore", "?")
                match_date = fixture.get("dateEvent", "Unknown")
                
                print(f"   {i+1}. {home_team} {home_score} - {away_score} {away_team} ({match_date})")
        else:
            print("❌ No recent results found")
        
        # Test 3: Check all leagues
        print(f"\n🏆 Available leagues:")
        for league_name, league_id in THESPORTSDB_LEAGUES.items():
            print(f"   {league_name} (ID: {league_id})")
        
        print("\n✅ TheSportsDB API is working correctly!")
        return True

async def sync_matches():
    """Sync matches from TheSportsDB"""
    print("\n🚀 Starting match synchronization from TheSportsDB...")
    
    # Get database session
    db = next(get_db())
    service = TheSportsDBService(db)
    
    try:
        # Sync all leagues
        stats = await service.sync_all_leagues()
        
        print(f"\n📊 SYNC RESULTS:")
        print(f"   Fetched: {stats['fetched']} matches")
        print(f"   Created: {stats['created']} new matches")
        print(f"   Updated: {stats['updated']} existing matches")
        print(f"   Errors: {stats['errors']} errors")
        
        if stats['errors'] == 0:
            print("✅ All leagues synced successfully!")
        else:
            print(f"⚠️  Completed with {stats['errors']} errors")
        
        return stats
        
    except Exception as e:
        print(f"❌ Error syncing matches: {e}")
        return {"fetched": 0, "created": 0, "updated": 0, "errors": 1}
    finally:
        db.close()

async def main():
    """Main function"""
    print("🚀 TheSportsDB Match Sync")
    print("=" * 50)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        # Test API only
        await test_api_connection()
    else:
        # Test API first, then sync
        success = await test_api_connection()
        
        if success:
            await sync_matches()
            
            print(f"\n🎉 Sync completed!")
            print(f"🔄 Refresh your browser to see real match data from:")
            print(f"   • Premier League")
            print(f"   • La Liga") 
            print(f"   • Serie A")
            print(f"   • Bundesliga")
            print(f"   • Ligue 1")
            print(f"   • Champions League")
            print(f"   • Europa League")
        else:
            print("\n❌ API test failed. Cannot sync matches.")

if __name__ == "__main__":
    asyncio.run(main())