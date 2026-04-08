"""
Add test stream URLs to existing matches
"""
from app.core.database import SessionLocal
from app.models.match import Match

def add_test_streams():
    db = SessionLocal()
    
    # Sample HLS stream URLs for testing
    test_streams = [
        "https://demo.unified-streaming.com/k8s/features/stable/video/tears-of-steel/tears-of-steel.ism/.m3u8",
        "https://bitdash-a.akamaihd.net/content/sintel/hls/playlist.m3u8",
        "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8",
        "https://demo.unified-streaming.com/k8s/features/stable/video/tears-of-steel/tears-of-steel.ism/.m3u8",
        "https://bitdash-a.akamaihd.net/content/MI201109210084_1/m3u8s/f08e80da-bf1d-4e3d-8899-f0f6155f6efa.m3u8"
    ]
    
    try:
        # Get first 5 matches
        matches = db.query(Match).limit(5).all()
        
        for i, match in enumerate(matches):
            if i < len(test_streams):
                match.stream_url = test_streams[i]
                print(f"Added stream URL to match {match.id}: {match.title}")
        
        db.commit()
        print(f"✅ Successfully added stream URLs to {len(matches)} matches")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_test_streams()