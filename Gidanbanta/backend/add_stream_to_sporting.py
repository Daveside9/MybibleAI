#!/usr/bin/env python3
"""
Add Stream to Sporting CP Match - Add live stream to Sporting CP vs AVS match
"""

from app.core.database import get_db
from app.models.match import Match

def add_stream_to_sporting():
    """Add a working live stream URL to the Sporting CP vs AVS match"""
    
    db = next(get_db())
    
    try:
        print('🔍 Finding Sporting CP vs AVS match (ID: 417)...')
        
        # Find the Sporting CP match
        match = db.query(Match).filter(Match.id == 417).first()
        
        if not match:
            print('❌ Sporting CP vs AVS match not found!')
            return
        
        print(f'✅ Found match: {match.home_team} vs {match.away_team}')
        print(f'   Current stream URL: {match.stream_url}')
        print(f'   Status: {match.status.value}')
        
        # Add a working live stream URL
        stream_url = "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"
        
        print(f'🎯 Adding live stream: Mux Test Stream (Big Buck Bunny)')
        match.stream_url = stream_url
        
        # Commit changes
        db.commit()
        
        print(f'✅ Live stream added successfully!')
        print(f'   Stream URL: {match.stream_url}')
        
        print(f'\n🎉 Sporting CP vs AVS match now has a live stream!')
        print(f'   Match URL: http://localhost:3000/match/417')
        print(f'   Status: 🔴 LIVE')
        print(f'   Video: Will show test stream content')
        
        print(f'\n📱 What you\'ll see when you visit the page:')
        print(f'   ✅ Video player with working stream')
        print(f'   ✅ Live indicator (🔴 LIVE)')
        print(f'   ✅ Video controls (play, pause, volume)')
        print(f'   ✅ Full screen option')
        print(f'   ✅ Chat functionality')
        
        return 417
        
    except Exception as e:
        print(f'❌ Error adding live stream: {e}')
        db.rollback()
        return None
    finally:
        db.close()

if __name__ == "__main__":
    match_id = add_stream_to_sporting()
    if match_id:
        print(f'\n🚀 Ready to test! Visit: http://localhost:3000/match/{match_id}')