#!/usr/bin/env python3
"""
Create live matches with stream URLs for testing
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.core.database import SessionLocal
from backend.app.models.match import Match, MatchStatus
from datetime import datetime

def create_live_matches():
    """Create some live matches with stream URLs for testing"""
    
    db = SessionLocal()
    
    # Test stream URLs
    test_streams = [
        "https://demo.unified-streaming.com/k8s/features/stable/video/tears-of-steel/tears-of-steel.ism/.m3u8",
        "https://bitdash-a.akamaihd.net/content/sintel/hls/playlist.m3u8",
        "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8",
    ]
    
    try:
        # Get first 3 matches and make them live with streams
        matches = db.query(Match).limit(3).all()
        
        print("🔴 Creating Live Matches with Streams")
        print("=" * 50)
        
        for i, match in enumerate(matches):
            # Set to LIVE status
            match.status = MatchStatus.LIVE
            match.stream_url = test_streams[i % len(test_streams)]
            match.started_at = datetime.utcnow()
            
            print(f"✅ Match {match.id}: {match.home_team} vs {match.away_team}")
            print(f"   Status: LIVE")
            print(f"   Stream: {match.stream_url}")
            print()
        
        db.commit()
        print(f"🎬 Successfully created {len(matches)} live matches with streams!")
        
        # Also set some matches to different statuses for variety
        other_matches = db.query(Match).offset(3).limit(5).all()
        statuses = [MatchStatus.SCHEDULED, MatchStatus.FINISHED, MatchStatus.POSTPONED]
        
        for i, match in enumerate(other_matches):
            match.status = statuses[i % len(statuses)]
            if match.status == MatchStatus.FINISHED:
                match.home_score = 2
                match.away_score = 1
        
        db.commit()
        print(f"📊 Updated {len(other_matches)} additional matches with various statuses")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_live_matches()