#!/usr/bin/env python3
"""
Check Missing Matches - Find which match IDs are missing after deletion
"""

from app.core.database import get_db
from app.models.match import Match

def check_missing_matches():
    """Check which match IDs are missing after deletion"""
    
    db = next(get_db())
    
    try:
        print('🔍 Checking for missing match IDs...')
        
        # Get all existing match IDs
        existing_matches = db.query(Match.id).all()
        existing_ids = [match.id for match in existing_matches]
        
        print(f'   Found {len(existing_ids)} existing matches')
        print(f'   ID range: {min(existing_ids)} to {max(existing_ids)}')
        
        # Check for gaps in the sequence
        all_ids_in_range = set(range(min(existing_ids), max(existing_ids) + 1))
        missing_ids = all_ids_in_range - set(existing_ids)
        
        if missing_ids:
            missing_list = sorted(list(missing_ids))
            print(f'\n❌ Found {len(missing_ids)} missing match IDs:')
            print(f'   Missing IDs: {missing_list[:20]}{"..." if len(missing_list) > 20 else ""}')
            
            # These are likely the deleted mock matches
            print(f'\n💡 These are likely the 35 mock matches that were deleted')
            print(f'   If users try to access these match IDs, they will get "Failed to fetch" errors')
        else:
            print(f'\n✅ No missing match IDs found - sequence is continuous')
        
        # Show some sample existing matches
        sample_matches = db.query(Match).limit(5).all()
        print(f'\n📋 Sample existing matches:')
        for match in sample_matches:
            print(f'   ID {match.id}: {match.home_team} vs {match.away_team} | External ID: {match.external_id}')
        
    except Exception as e:
        print(f'❌ Error checking missing matches: {e}')
    finally:
        db.close()

if __name__ == "__main__":
    check_missing_matches()