#!/usr/bin/env python3
"""
Remove all mock matches from the database
This script will delete matches that have no external_id or external_id = 0
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import get_db
from app.models.match import Match
from sqlalchemy.orm import Session

def remove_mock_matches():
    """Remove all mock matches from the database"""
    
    # Get database session
    db = next(get_db())
    
    try:
        print("Scanning for mock matches...")
        print("=" * 50)
        
        # Find all mock matches (no external_id or external_id = 0)
        mock_matches = db.query(Match).filter(
            (Match.external_id.is_(None)) | (Match.external_id == 0)
        ).all()
        
        print(f"Found {len(mock_matches)} mock matches:")
        print()
        
        # List all mock matches before deletion
        for i, match in enumerate(mock_matches, 1):
            print(f"{i}. {match.title}")
            print(f"   ID: {match.id}")
            print(f"   External ID: {match.external_id}")
            print(f"   Scheduled: {match.scheduled_at}")
            print(f"   League ID: {match.league_id}")
            print()
        
        if not mock_matches:
            print("No mock matches found! All matches have valid external IDs.")
            return
        
        # Confirm deletion
        print(f"About to delete {len(mock_matches)} mock matches.")
        confirm = input("Are you sure you want to proceed? (yes/no): ").lower().strip()
        
        if confirm not in ['yes', 'y']:
            print("Operation cancelled.")
            return
        
        # Delete mock matches
        deleted_count = 0
        for match in mock_matches:
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
        print(f"Successfully deleted {deleted_count} mock matches!")
        print("Database cleanup complete.")
        
        # Verify cleanup
        remaining_mock_matches = db.query(Match).filter(
            (Match.external_id.is_(None)) | (Match.external_id == 0)
        ).count()
        
        if remaining_mock_matches == 0:
            print("✅ Verification: No mock matches remaining in database.")
        else:
            print(f"⚠️  Warning: {remaining_mock_matches} mock matches still remain.")
        
        # Show total real matches
        real_matches_count = db.query(Match).filter(
            Match.external_id.isnot(None),
            Match.external_id > 0
        ).count()
        
        print(f"📊 Total real matches in database: {real_matches_count}")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    remove_mock_matches()