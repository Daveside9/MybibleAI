#!/usr/bin/env python3
"""
Add Live Stream - Add a working live stream URL to the Arsenal match
"""

from app.core.database import get_db
from app.models.match import Match

def add_live_stream():
    """Add a working live stream URL to the Arsenal vs Wolves match"""
    
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
        print(f'   Status: {match.status.value}')
        
        # Working live stream URLs for testing
        stream_options = {
            1: {
                "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8",
                "name": "Mux Test Stream (Big Buck Bunny)",
                "description": "High quality test stream that works reliably"
            },
            2: {
                "url": "https://bitdash-a.akamaihd.net/content/sintel/hls/playlist.m3u8",
                "name": "Bitdash Test Stream (Sintel)",
                "description": "Another reliable test stream"
            },
            3: {
                "url": "https://demo.unified-streaming.com/k8s/features/stable/video/tears-of-steel/tears-of-steel.ism/.m3u8",
                "name": "Unified Streaming (Tears of Steel)",
                "description": "Demo stream from Unified Streaming"
            },
            4: {
                "url": "https://cph-p2p-msl.akamaized.net/hls/live/2000341/test/master.m3u8",
                "name": "Akamai Test Stream",
                "description": "Live test stream from Akamai CDN"
            }
        }
        
        print(f'\n📺 Available live stream options:')
        for key, option in stream_options.items():
            print(f'   {key}. {option["name"]}')
            print(f'      URL: {option["url"]}')
            print(f'      Description: {option["description"]}')
            print()
        
        # Let's use option 1 (Mux test stream) as it's very reliable
        selected_option = stream_options[1]
        
        print(f'🎯 Adding live stream: {selected_option["name"]}')
        match.stream_url = selected_option["url"]
        
        # Commit changes
        db.commit()
        
        print(f'✅ Live stream added successfully!')
        print(f'   Stream URL: {match.stream_url}')
        print(f'   Stream Name: {selected_option["name"]}')
        
        print(f'\n🎉 Arsenal vs Wolves match now has a live stream!')
        print(f'   Match URL: http://localhost:3000/match/230')
        print(f'   Status: 🔴 LIVE')
        print(f'   Video: Will show {selected_option["name"]}')
        
        print(f'\n📱 What you\'ll see when you refresh the page:')
        print(f'   ✅ Video player with working stream')
        print(f'   ✅ Live indicator (🔴 LIVE)')
        print(f'   ✅ Video controls (play, pause, volume)')
        print(f'   ✅ Full screen option')
        print(f'   ✅ Chat functionality')
        
        print(f'\n💡 Note: This is a test stream for demonstration.')
        print(f'   For real football matches, you\'d need to integrate with')
        print(f'   legitimate streaming providers that have broadcasting rights.')
        
    except Exception as e:
        print(f'❌ Error adding live stream: {e}')
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_live_stream()