"""
Celery Tasks for Match Synchronization
Periodic background jobs to keep match data up-to-date
"""
import logging
from datetime import datetime, timedelta
from app.celery_app import celery_app
from app.database import SessionLocal
from app.services.match_service import MatchService

logger = logging.getLogger(__name__)


@celery_app.task(name="app.tasks.match_sync.sync_live_matches", bind=True, max_retries=3)
def sync_live_matches(self):
    """
    Celery task to sync live matches
    Runs every 5 minutes to update scores and status of live matches
    """
    db = SessionLocal()
    try:
        logger.info("Starting live matches sync task")
        
        # Create match service
        match_service = MatchService(db)
        
        # Update live matches (synchronous wrapper for async method)
        import asyncio
        stats = asyncio.run(match_service.update_live_matches())
        
        logger.info(f"Live matches sync completed: {stats}")
        return {
            "status": "success",
            "timestamp": datetime.utcnow().isoformat(),
            "stats": stats
        }
        
    except Exception as e:
        logger.error(f"Error in sync_live_matches task: {e}")
        # Retry with exponential backoff
        raise self.retry(exc=e, countdown=60 * (2 ** self.request.retries))
    
    finally:
        db.close()


@celery_app.task(name="app.tasks.match_sync.sync_scheduled_matches", bind=True, max_retries=3)
def sync_scheduled_matches(self):
    """
    Celery task to sync scheduled matches
    Runs every 30 minutes to fetch upcoming matches for the next 14 days
    """
    db = SessionLocal()
    try:
        logger.info("Starting scheduled matches sync task")
        
        # Create match service
        match_service = MatchService(db)
        
        # Sync next 14 days (synchronous wrapper for async method)
        import asyncio
        stats = asyncio.run(match_service.sync_next_14_days())
        
        logger.info(f"Scheduled matches sync completed: {stats}")
        return {
            "status": "success",
            "timestamp": datetime.utcnow().isoformat(),
            "stats": stats
        }
        
    except Exception as e:
        logger.error(f"Error in sync_scheduled_matches task: {e}")
        # Retry with exponential backoff
        raise self.retry(exc=e, countdown=60 * (2 ** self.request.retries))
    
    finally:
        db.close()


@celery_app.task(name="app.tasks.match_sync.sync_specific_date_range")
def sync_specific_date_range(date_from: str, date_to: str, league_id: int = None):
    """
    Manual task to sync matches for a specific date range
    Can be triggered manually via admin interface
    
    Args:
        date_from: Start date (YYYY-MM-DD)
        date_to: End date (YYYY-MM-DD)
        league_id: Optional league ID filter
    """
    db = SessionLocal()
    try:
        logger.info(f"Starting manual sync: {date_from} to {date_to}, league: {league_id}")
        
        # Create match service
        match_service = MatchService(db)
        
        # Sync specified date range
        import asyncio
        stats = asyncio.run(
            match_service.sync_matches(
                date_from=date_from,
                date_to=date_to,
                league_id=league_id
            )
        )
        
        logger.info(f"Manual sync completed: {stats}")
        return {
            "status": "success",
            "timestamp": datetime.utcnow().isoformat(),
            "date_from": date_from,
            "date_to": date_to,
            "league_id": league_id,
            "stats": stats
        }
        
    except Exception as e:
        logger.error(f"Error in sync_specific_date_range task: {e}")
        return {
            "status": "error",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e)
        }
    
    finally:
        db.close()
