#!/usr/bin/env python3
"""
Verify Sporting Match - Check if the match exists in database
"""

from app.core.database import get_db
from app.models.match import Match

def verify_sporting_match():
    """Verify the Sporting CP match exists in database"""
    
    db = next(get_db())
    
    try:
        print('🔍 Verifying Sporting CP vs AVS match (ID: 417)...')
        
        # Find the match
        match = db.query(Match).filter(Match.id == 417).first()
        
        if not match:
            print('❌ Match ID 417 not found in database!')
            
            # Let's check what matches do exist
            print('\n🔍 Checking available matches...')
            recent_matches = db.query(Match).order_by(Match.id.desc()).limit(10).all()
            
            print(f'📋 Last 10 matches in database:')
            for m in recent_matches:
                print(f'   ID: {m.id} - {m.home_team} vs {m.away_team} ({m.status.value})')
            
            return False
        
        print(f'✅ Match found in database:')
        print(f'   ID: {match.id}')
        print(f'   Match: {match.home_team} vs {match.away_team}')
        print(f'   Status: {match.status.value}')
        print(f'   Stream URL: {match.stream_url}')
        print(f'   External ID: {match.external_id}')
        print(f'   Scheduled: {match.scheduled_at}')
        
        return True
        
    except Exception as e:
        print(f'❌ Error verifying match: {e}')
        return False
    finally:
        db.close()

if __name__ == "__main__":
    verify_sporting_match()