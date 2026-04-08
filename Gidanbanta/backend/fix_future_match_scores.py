#!/usr/bin/env python3
"""
Fix Future Match Scores - Remove scores from matches scheduled in the future
"""

from app.core.database import get_db
from app.models.match import Match
from sqlalchemy import or_
from datetime import datetime

def fix_future_match_scores():
    """Remove scores from matches scheduled in the future"""
    
    db = next(get_db())
    
    try:
        print('🔧 Fixing future matches with scores...')
        
        current_time = datetime.now()
        print(f'   Current time: {current_time}')
        
        # Find future matches that have scores
        future_matches_with_scores = db.query(Match).filter(
            Match.scheduled_at > current_time,
            or_(Match.home_score.isnot(None), Match.away_score.isnot(None))
        ).all()
        
        print(f'   Found {len(future_matches_with_scores)} future matches with scores')
        
        if not future_matches_with_scores:
            print('✅ No future matches with scores found!')
            return
        
        # Show some examples
        print(f'\n📋 Examples of matches to fix:')
        for i, match in enumerate(future_matches_with_scores[:5], 1):
            score = f"{match.home_score or 0}-{match.away_score or 0}"
            print(f'   {i}. {match.home_team} vs {match.away_team}')
            print(f'      Score: {score} | Scheduled: {match.scheduled_at}')
        
        if len(future_matches_with_scores) > 5:
            print(f'   ... and {len(future_matches_with_scores) - 5} more matches')
        
        # Remove scores from future matches
        print(f'\n🗑️  Removing scores from {len(future_matches_with_scores)} future matches...')
        
        updated_count = 0
        for match in future_matches_with_scores:
            # Clear the scores
            match.home_score = None
            match.away_score = None
            
            # Set status to scheduled if it was finished
            if match.status.value == 'finished':
                from app.models.match import MatchStatus
                match.status = MatchStatus.SCHEDULED
            
            updated_count += 1
            
            if updated_count % 50 == 0:
                print(f'   Updated {updated_count}/{len(future_matches_with_scores)} matches...')
        
        # Commit changes
        db.commit()
        
        print(f'\n✅ Successfully fixed {updated_count} future matches!')
        print(f'   Removed scores from all future matches')
        print(f'   Set finished matches back to scheduled status')
        
        # Verify the fix
        remaining_future_with_scores = db.query(Match).filter(
            Match.scheduled_at > current_time,
            or_(Match.home_score.isnot(None), Match.away_score.isnot(None))
        ).count()
        
        if remaining_future_with_scores == 0:
            print(f'\n🎉 Perfect! No future matches have scores anymore')
        else:
            print(f'\n⚠️  Warning: {remaining_future_with_scores} future matches still have scores')
        
        # Show current status
        total_matches = db.query(Match).count()
        matches_with_scores = db.query(Match).filter(
            or_(Match.home_score.isnot(None), Match.away_score.isnot(None))
        ).count()
        
        print(f'\n📊 Database status:')
        print(f'   Total matches: {total_matches}')
        print(f'   Matches with scores: {matches_with_scores}')
        print(f'   Matches without scores: {total_matches - matches_with_scores}')
        
    except Exception as e:
        print(f'❌ Error fixing future match scores: {e}')
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    fix_future_match_scores()