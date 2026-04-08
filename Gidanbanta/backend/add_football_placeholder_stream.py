#!/usr/bin/env python3
"""
Add Football Placeholder Stream - Replace test video with football-specific placeholder
"""

from app.core.database import get_db
from app.models.match import Match

def add_football_placeholder_stream():
    """Add a football-specific placeholder stream to the Sporting CP match"""
    
    db = next(get_db())
    
    try:
        print('🔍 Finding Sporting CP vs AVS match (ID: 417)...')
        
        # Find the match
        match = db.query(Match).filter(Match.id == 417).first()
        
        if not match:
            print('❌ Match not found!')
            return
        
        print(f'✅ Found match: {match.home_team} vs {match.away_team}')
        print(f'   Current stream URL: {match.stream_url}')
        
        # Instead of a test video, let's set stream_url to None
        # This will trigger the VideoPlayer to show "No Stream Available" 
        # which is more appropriate than a cartoon video
        
        print('🎯 Removing test video stream (will show "Live Match" placeholder)...')
        match.stream_url = None
        
        # Commit changes
        db.commit()
        
        print('✅ Test video removed successfully!')
        print(f'\n📱 Now when you visit the match page, you\'ll see:')
        print(f'   ✅ "No Stream Available" message instead of cartoon video')
        print(f'   ✅ Live indicator (🔴 LIVE)')
        print(f'   ✅ Proper football match info')
        print(f'   ✅ Chat functionality')
        
        print(f'\n💡 To add a real football stream:')
        print(f'   1. Get a real streaming URL from a sports API')
        print(f'   2. Update match.stream_url with the real URL')
        print(f'   3. Real streams typically use HLS (.m3u8) or DASH formats')
        
        return True
        
    except Exception as e:
        print(f'❌ Error updating stream: {e}')
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    add_football_placeholder_stream()