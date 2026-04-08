#!/usr/bin/env python3
"""
Remove all finished matches from the database
This script will delete matches with status 'FINISHED' or 'COMPLETED'
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import get_db
from app.models.match import Match, MatchStatus
from sqlalchemy.orm import Session
from datetime import datetime

def remove_finished_matches():
    """Remove all finished matches from the database"""
    
    # Get database session
    db = next(get_db())
    
    try:
        print("Scanning for finished matches...")
        print("=" * 50)
        
        # First, let's see what statuses exist
        all_statuses = db.query(Match.status).distinct().all()
        print("Current match statuses in database:")
        for status in all_statuses:
            count = db.query(Match).filter(Match.status == status[0]).count()
            print(f"  - {status[0]}: {count} matches")
        
        print()
        
        # Find finished matches
        finished_matches = db.query(Match).filter(
            Match.status == MatchStatus.FINISHED
        ).all()
        
        print(f"Found {len(finished_matches)} finished matches:")
        print()
        
        # List finished matches before deletion
        for i, match in enumerate(finished_matches, 1):
            print(f"{i}. {match.title}")
            print(f"   ID: {match.id}")
            print(f"   Status: {match.status}")
            print(f"   Scheduled: {match.scheduled_at}")
            print(f"   Score: {match.home_score} - {match.away_score}")
            print()
        
        if not finished_matches:
            print("No finished matches found!")
            
            # Show what matches we do have
            print("Current matches by status:")
            for status in all_statuses:
                matches = db.query(Match).filter(Match.status == status[0]).limit(3).all()
                print(f"\n{status[0]} matches (showing first 3):")
                for match in matches:
                    print(f"  - {match.title}")
            return
        
        # Confirm deletion
        print(f"About to delete {len(finished_matches)} finished matches.")
        confirm = input("Are you sure you want to proceed? (yes/no): ").lower().strip()
        
        if confirm not in ['yes', 'y']:
            print("Operation cancelled.")
            return
        
        # Delete finished matches
        deleted_count = 0
        for match in finished_matches:
            try:
                db.delete(match)
                deleted_count += 1
                print(f"Deleted: {match.title}")
            except Exception as e:
                print(f"Error deleting {match.title}: {e}")
        
        # Commit changes
        db.commit()
        
        print()
        print("=" * 50)
        print(f"Successfully deleted {deleted_count} finished matches!")
        print("Database cleanup complete.")
        
        # Show remaining matches
        remaining_matches = db.query(Match).count()
        print(f"📊 Total matches remaining: {remaining_matches}")
        
        # Show status distribution after cleanup
        print("\nRemaining matches by status:")
        remaining_statuses = db.query(Match.status).distinct().all()
        for status in remaining_statuses:
            count = db.query(Match).filter(Match.status == status[0]).count()
            print(f"  - {status[0]}: {count} matches")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    remove_finished_matches()