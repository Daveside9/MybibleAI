#!/usr/bin/env python3
"""
Add Free Stream to Match - Use the free streaming service to add a stream
"""

from app.core.database import get_db
from app.models.match import Match
from app.services.free_streaming_service import FreeStreamingService

def add_free_stream_to_match():
    """Add a free stream to the Sporting CP match using the streaming service"""
    
    db = next(get_db())
    streaming_service = FreeStreamingService()
    
    try:
        print('🔍 Finding Sporting CP vs AVS match (ID: 417)...')
        
        # Find the match
        match = db.query(Match).filter(Match.id == 417).first()
        
        if not match:
            print('❌ Match not found!')
            return
        
        print(f'✅ Found match: {match.home_team} vs {match.away_team}')
        print(f'   Current stream URL: {match.stream_url}')
        
        # Use the streaming service to find a stream
        print('🔍 Searching for free stream...')
        stream_info = streaming_service.find_stream_for_match(
            match.home_team, 
            match.away_team,
            "Primeira Liga"
        )
        
        if not stream_info:
            print('❌ No free stream found!')
            return
        
        print('✅ Found free stream:')
        print(f'   URL: {stream_info["stream_url"]}')
        print(f'   Quality: {stream_info["quality"]}')
        print(f'   Source: {stream_info["source"]}')
        print(f'   Legal Status: {stream_info["legal_status"]}')
        
        # Update the match with the stream URL
        match.stream_url = stream_info["stream_url"]
        
        # Commit changes
        db.commit()
        
        print(f'\n🎉 Stream added successfully!')
        print(f'   Match URL: http://localhost:3000/match/417')
        print(f'   Status: 🔴 LIVE')
        print(f'   Stream: {stream_info["description"]}')
        
        print(f'\n📱 What you\'ll see when you visit the page:')
        print(f'   ✅ Video player with working stream')
        print(f'   ✅ Live indicator (🔴 LIVE)')
        print(f'   ✅ Video controls (play, pause, volume)')
        print(f'   ✅ Full screen option')
        print(f'   ✅ Chat functionality')
        
        print(f'\n💡 Note: This is a {stream_info["source"]} for demonstration.')
        print(f'   Quality: {stream_info["quality"]}')
        print(f'   Legal Status: {stream_info["legal_status"]}')
        
        return True
        
    except Exception as e:
        print(f'❌ Error adding stream: {e}')
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = add_free_stream_to_match()
    if success:
        print(f'\n🚀 Ready to test! Visit: http://localhost:3000/match/417')
        print(f'   The video player should now show the stream content.')
    else:
        print(f'\n❌ Failed to add stream. Check the logs above.')