#!/usr/bin/env python3
"""
Sync Real Football Matches
Fetches real match data from RapidAPI Football API for major leagues
"""
import asyncio
import sys
import os
from datetime import datetime, timedelta

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import get_db
from app.services.match_service import MatchService
from app.core.config import settings

# Major League IDs from API-Football
MAJOR_LEAGUES = {
    "Premier League": 39,      # English Premier League
    "La Liga": 140,           # Spanish La Liga
    "Serie A": 135,           # Italian Serie A
    "Bundesliga": 78,         # German Bundesliga
    "Ligue 1": 61,           # French Ligue 1
    "Champions League": 2,    # UEFA Champions League
    "Europa League": 3,       # UEFA Europa League
    "Conference League": 848, # UEFA Conference League
}

async def sync_league_matches(league_name: str, league_id: int, days_ahead: int = 14):
    """Sync matches for a specific league"""
    print(f"\n🔄 Syncing {league_name} (ID: {league_id})...")
    
    # Get database session
    db = next(get_db())
    match_service = MatchService(db)
    
    try:
        # Calculate date range
        today = datetime.now().date()
        end_date = today + timedelta(days=days_ahead)
        
        # Sync matches
        stats = await match_service.sync_matches(
            date_from=str(today),
            date_to=str(end_date),
            league_id=league_id
        )
        
        print(f"✅ {league_name}: Fetched {stats['fetched']}, Created {stats['created']}, Updated {stats['updated']}, Errors {stats['errors']}")
        return stats
        
    except Exception as e:
        print(f"❌ Error syncing {league_name}: {e}")
        return {"fetched": 0, "created": 0, "updated": 0, "errors": 1}
    finally:
        db.close()

async def sync_all_leagues():
    """Sync matches for all major leagues"""
    print("🚀 Starting real match synchronization...")
    print(f"📅 Syncing matches for the next 14 days")
    print(f"🔑 Using API Key: {settings.FOOTBALL_API_KEY[:20]}...")
    
    total_stats = {"fetched": 0, "created": 0, "updated": 0, "errors": 0}
    
    # Sync each league
    for league_name, league_id in MAJOR_LEAGUES.items():
        stats = await sync_league_matches(league_name, league_id)
        
        # Add to totals
        for key in total_stats:
            total_stats[key] += stats.get(key, 0)
        
        # Small delay between requests to respect rate limits
        await asyncio.sleep(1)
    
    print(f"\n📊 TOTAL RESULTS:")
    print(f"   Fetched: {total_stats['fetched']} matches")
    print(f"   Created: {total_stats['created']} new matches")
    print(f"   Updated: {total_stats['updated']} existing matches")
    print(f"   Errors: {total_stats['errors']} errors")
    
    if total_stats['errors'] == 0:
        print("✅ All leagues synced successfully!")
    else:
        print(f"⚠️  Completed with {total_stats['errors']} errors")

async def sync_live_matches():
    """Sync currently live matches"""
    print("\n🔴 Syncing live matches...")
    
    db = next(get_db())
    match_service = MatchService(db)
    
    try:
        stats = await match_service.update_live_matches()
        print(f"✅ Live matches: Fetched {stats['fetched']}, Updated {stats['updated']}, Errors {stats['errors']}")
        return stats
    except Exception as e:
        print(f"❌ Error syncing live matches: {e}")
        return {"fetched": 0, "updated": 0, "errors": 1}
    finally:
        db.close()

async def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] == "--live":
        # Sync only live matches
        await sync_live_matches()
    else:
        # Sync all leagues
        await sync_all_leagues()
        
        # Also sync live matches
        await sync_live_matches()

if __name__ == "__main__":
    asyncio.run(main())