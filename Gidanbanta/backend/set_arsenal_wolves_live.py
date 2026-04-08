#!/usr/bin/env python3
"""
Set Arsenal vs Wolves Live - Update the match status to live for streaming
"""

from app.core.database import get_db
from app.models.match import Match, MatchStatus
from datetime import datetime

def set_arsenal_wolves_live():
    """Set Arsenal vs Wolverhampton match to live status"""
    
    db = next(get_db())
    
    try:
        print('🔍 Finding Arsenal vs Wolverhampton match...')
        
        # Find the Arsenal vs Wolves match
        match = db.query(Match).filter(
            Match.id == 230  # We know it's ID 230 from the previous search
        ).first()
        
        if not match:
            print('❌ Arsenal vs Wolves match not found!')
            return
        
        print(f'✅ Found match: {match.home_team} vs {match.away_team}')
        print(f'   Current status: {match.status.value}')
        print(f'   Match ID: {match.id}')
        
        # Update status to live
        print(f'\n🔴 Setting match to LIVE status...')
        match.status = MatchStatus.LIVE
        match.started_at = datetime.utcnow()
        
        # Commit changes
        db.commit()
        
        print(f'✅ Match updated successfully!')
        print(f'   Status: {match.status.value}')
        print(f'   Started at: {match.started_at}')
        
        print(f'\n🎯 You can now stream the match at:')
        print(f'   URL: http://localhost:3000/match/{match.id}')
        print(f'   Match: {match.home_team} vs {match.away_team}')
        print(f'   Status: 🔴 LIVE')
        
        # Verify the change
        updated_match = db.query(Match).filter(Match.id == 230).first()
        if updated_match and updated_match.status == MatchStatus.LIVE:
            print(f'\n✅ Verification successful - match is now LIVE!')
        else:
            print(f'\n❌ Verification failed - something went wrong')
        
    except Exception as e:
        print(f'❌ Error setting match to live: {e}')
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    set_arsenal_wolves_live()