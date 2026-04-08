#!/usr/bin/env python3
"""
Add Stream URL to Arsenal Match - Add a real stream URL for testing
"""

from app.core.database import get_db
from app.models.match import Match

def add_stream_url_arsenal():
    """Add a stream URL to the Arsenal vs Wolves match"""
    
    db = next(get_db())
    
    try:
        print('🔍 Finding Arsenal vs Wolverhampton match...')
        
        # Find the Arsenal vs Wolves match
        match = db.query(Match).filter(Match.id == 230).first()
        
        if not match:
            print('❌ Arsenal vs Wolves match not found!')
            return
        
        print(f'✅ Found match: {match.home_team} vs {match.away_team}')
        print(f'   Current stream URL: {match.stream_url}')
        
        # You can choose from these options:
        stream_options = {
            1: "https://demo.unified-streaming.com/k8s/features/stable/video/tears-of-steel/tears-of-steel.ism/.m3u8",  # Demo movie
            2: "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8",  # Test stream
            3: "https://bitdash-a.akamaihd.net/content/sintel/hls/playlist.m3u8",  # Another test stream
            4: None  # No stream (will show "No Stream Available")
        }
        
        print(f'\n📺 Stream URL options:')
        print(f'   1. Demo movie (Tears of Steel)')
        print(f'   2. Test stream (Mux)')
        print(f'   3. Test stream (Sintel)')
        print(f'   4. No stream (show "No Stream Available")')
        
        # For now, let's set it to None so it shows the proper message
        choice = 4
        selected_url = stream_options[choice]
        
        print(f'\n🔧 Setting stream URL to option {choice}...')
        match.stream_url = selected_url
        
        # Commit changes
        db.commit()
        
        print(f'✅ Stream URL updated successfully!')
        print(f'   New stream URL: {match.stream_url or "None (will show No Stream Available)"}')
        
        print(f'\n🎯 Now when you refresh the match page:')
        if selected_url:
            print(f'   - Video player will show the stream')
        else:
            print(f'   - Video player will show "No Stream Available" message')
            print(f'   - This is the correct behavior for matches without real streams')
        
    except Exception as e:
        print(f'❌ Error updating stream URL: {e}')
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_stream_url_arsenal()