#!/usr/bin/env python3
"""
Find Problematic Match Links - Identify which match IDs might be causing issues
"""

from app.core.database import get_db
from app.models.match import Match

def find_problematic_match_links():
    """Find which match IDs might be causing the 'Failed to fetch' error"""
    
    db = next(get_db())
    
    try:
        print('🔍 Analyzing match IDs to find potential issues...')
        
        # Get all existing match IDs
        existing_matches = db.query(Match.id, Match.home_team, Match.away_team, Match.external_id).all()
        existing_ids = [match.id for match in existing_matches]
        
        print(f'   Found {len(existing_ids)} existing matches')
        print(f'   ID range: {min(existing_ids)} to {max(existing_ids)}')
        
        # Find gaps in the sequence (these are the deleted mock matches)
        all_ids_in_range = set(range(1, max(existing_ids) + 1))
        missing_ids = sorted(list(all_ids_in_range - set(existing_ids)))
        
        print(f'\n❌ Missing match IDs (deleted mock matches): {len(missing_ids)}')
        print(f'   IDs: {missing_ids[:20]}{"..." if len(missing_ids) > 20 else ""}')
        
        # These are the IDs that will cause "Failed to fetch" if accessed
        print(f'\n⚠️  If you try to access any of these URLs, you\'ll get "Failed to fetch":')
        for i, match_id in enumerate(missing_ids[:10], 1):
            print(f'   {i}. http://localhost:3000/match/{match_id}')
        
        if len(missing_ids) > 10:
            print(f'   ... and {len(missing_ids) - 10} more URLs')
        
        # Show some working match URLs
        print(f'\n✅ Working match URLs (these will load correctly):')
        for i, match in enumerate(existing_matches[:5], 1):
            print(f'   {i}. http://localhost:3000/match/{match.id} - {match.home_team} vs {match.away_team}')
        
        # Check if there are any patterns in the missing IDs
        consecutive_ranges = []
        start = missing_ids[0] if missing_ids else 0
        end = start
        
        for i in range(1, len(missing_ids)):
            if missing_ids[i] == missing_ids[i-1] + 1:
                end = missing_ids[i]
            else:
                consecutive_ranges.append((start, end))
                start = missing_ids[i]
                end = start
        
        if missing_ids:
            consecutive_ranges.append((start, end))
        
        print(f'\n📊 Missing ID ranges:')
        for start, end in consecutive_ranges:
            if start == end:
                print(f'   Single ID: {start}')
            else:
                print(f'   Range: {start}-{end} ({end-start+1} IDs)')
        
        print(f'\n💡 Solution:')
        print(f'   1. Clear browser cache and bookmarks for match URLs')
        print(f'   2. Use only the dashboard to navigate to matches')
        print(f'   3. The error handling will now redirect you automatically')
        print(f'   4. If you see this error, the match was likely deleted')
        
    except Exception as e:
        print(f'❌ Error analyzing match links: {e}')
    finally:
        db.close()

if __name__ == "__main__":
    find_problematic_match_links()