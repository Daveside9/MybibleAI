#!/usr/bin/env python3
"""
Delete All Mock Matches - Safe Version
Removes all test/mock matches and their related data safely
"""

from app.core.database import get_db
from app.models.match import Match
from sqlalchemy import or_, text

def delete_mock_matches_safe():
    """Safely delete all mock/test matches and their related data"""
    
    db = next(get_db())
    
    try:
        print('🗑️  Identifying mock matches for safe deletion...')
        
        # Find all mock matches based on multiple criteria
        mock_matches = db.query(Match).filter(
            or_(
                # Matches with suspicious external IDs (999xxx - clearly test data)
                Match.external_id.between(999000, 999999),
                
                # Matches with test/demo stream URLs
                Match.stream_url.like('%demo%'),
                Match.stream_url.like('%test%'),
                Match.stream_url.like('%bitdash%'),
                Match.stream_url.like('%tears-of-steel%'),
                Match.stream_url.like('%sintel%'),
                
                # Matches without external_id or with external_id = 0
                Match.external_id.is_(None),
                Match.external_id == 0
            )
        ).all()
        
        print(f'Found {len(mock_matches)} mock matches to delete')
        
        if not mock_matches:
            print('✅ No mock matches found to delete!')
            return
        
        # Get match IDs for deletion
        mock_match_ids = [match.id for match in mock_matches]
        
        print(f'Mock match IDs to delete: {mock_match_ids[:10]}{"..." if len(mock_match_ids) > 10 else ""}')
        
        # Count before deletion
        total_before = db.query(Match).count()
        
        # Step 1: Delete related match_rooms first
        print('🗑️  Deleting related match rooms...')
        placeholders = ','.join(['?' for _ in mock_match_ids])
        rooms_deleted = db.execute(
            text(f"DELETE FROM match_rooms WHERE match_id IN ({placeholders})"),
            tuple(mock_match_ids)
        ).rowcount
        print(f'   Deleted {rooms_deleted} match rooms')
        
        # Step 2: Delete related transactions
        print('🗑️  Deleting related transactions...')
        transactions_deleted = db.execute(
            text(f"DELETE FROM transactions WHERE match_id IN ({placeholders})"),
            tuple(mock_match_ids)
        ).rowcount
        print(f'   Deleted {transactions_deleted} transactions')
        
        # Step 3: Now safely delete the matches
        print('🗑️  Deleting mock matches...')
        matches_deleted = db.execute(
            text(f"DELETE FROM matches WHERE id IN ({placeholders})"),
            tuple(mock_match_ids)
        ).rowcount
        print(f'   Deleted {matches_deleted} matches')
        
        # Commit all changes
        db.commit()
        
        # Count after deletion
        total_after = db.query(Match).count()
        real_matches = db.query(Match).filter(Match.external_id > 0).count()
        
        print(f'\\n✅ Mock match deletion completed!')
        print(f'   Before: {total_before} total matches')
        print(f'   After: {total_after} total matches')
        print(f'   Deleted: {total_before - total_after} mock matches')
        print(f'   Remaining real matches: {real_matches}')
        
        # Verify no mock matches remain
        remaining_mock = db.query(Match).filter(
            or_(
                Match.external_id.between(999000, 999999),
                Match.stream_url.like('%demo%'),
                Match.stream_url.like('%test%'),
                Match.stream_url.like('%bitdash%'),
                Match.external_id.is_(None),
                Match.external_id == 0
            )
        ).count()
        
        if remaining_mock == 0:
            print(f'\\n🎉 All mock matches successfully removed!')
            print(f'   Database now contains only real matches with valid external IDs')
            print(f'   No test/demo stream URLs remain')
        else:
            print(f'\\n⚠️  Warning: {remaining_mock} potential mock matches still remain')
            
    except Exception as e:
        print(f'❌ Error during mock match deletion: {e}')
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    delete_mock_matches_safe()