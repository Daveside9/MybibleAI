"""
Celery Application Configuration
Handles background task processing for match synchronization
"""
from celery import Celery
from celery.schedules import crontab
from app.core.config import settings

# Initialize Celery app
celery_app = Celery(
    "matchhang",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.tasks.match_sync"]
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

# Celery Beat Schedule - Periodic tasks
celery_app.conf.beat_schedule = {
    "sync-live-matches": {
        "task": "app.tasks.match_sync.sync_live_matches",
        "schedule": 300.0,  # Every 5 minutes (300 seconds)
        "options": {"expires": 240}  # Task expires after 4 minutes
    },
    "sync-scheduled-matches": {
        "task": "app.tasks.match_sync.sync_scheduled_matches",
        "schedule": 1800.0,  # Every 30 minutes (1800 seconds)
        "options": {"expires": 1500}  # Task expires after 25 minutes
    },
}

if __name__ == "__main__":
    celery_app.start()
