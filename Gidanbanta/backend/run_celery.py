"""
Celery Worker Startup Script
Run this to start the Celery worker and beat scheduler
"""
import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.celery_app import celery_app

if __name__ == "__main__":
    # Start Celery worker with beat scheduler
    celery_app.worker_main([
        "worker",
        "--loglevel=info",
        "--beat",  # Enable beat scheduler
        "--scheduler=celery.beat:PersistentScheduler",
        "--concurrency=2",  # Number of worker processes
    ])
