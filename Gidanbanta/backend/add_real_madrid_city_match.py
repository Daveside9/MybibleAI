#!/usr/bin/env python3
"""
Add Real Madrid vs Manchester City Match for Testing
This script adds a specific match happening today at 9 PM
"""
from datetime import datetime, timedelta
from app.core.database import SessionLocal
from app.models.match import Match, MatchStatus

def add_real_madrid_city_match():
    """Add Real Madrid vs Manchester City match for today at 9 PM"""
    
    print("⚽ Adding Real Madrid vs Manchester City Match")
    print("=" * 50)
    
    db = SessionLocal()
    
    try:
        # Calculate 9 PM today
        today = datetime.now().replace(hour=21, minute=0, second=0, microsecond=0)
        
        # Check if match already exists
        existing = db.query(Match).filter(
            Match.home_team == "Real Madrid",
            Match.away_team == "Manchester City"
        ).first()
        
        if existing:
            print("🔄 Match already exists - updating...")
            
            # Update the existing match
            existing.scheduled_at = today
            existing.status = MatchStatus.LIVE if datetime.now().hour >= 21 else MatchStatus.SCHEDULED
            existing.is_featured = True
            existing.stream_url = "https://demo.unified-streaming.com/k8s/features/stable/video/tears-of-steel/tears-of-steel.ism/.m3u8"
            
            # Add some realistic scores if live
            if existing.status == MatchStatus.LIVE:
                existing.home_score = 2
                existing.away_score = 1
            
            print(f"✅ Updated: {existing.title}")
            
        else:
            print("➕ Creating new match...")
            
            # Create new match
            match_data = {
                "external_id": 999999,  # Unique ID for this test match
                "title": "Real Madrid vs Manchester City",
                "home_team": "Real Madrid",
                "away_team": "Manchester City",
                "home_score": 2 if datetime.now().hour >= 21 else 0,
                "away_score": 1 if datetime.now().hour >= 21 else 0,
                "status": MatchStatus.LIVE if datetime.now().hour >= 21 else MatchStatus.SCHEDULED,
                "scheduled_at": today,
                "is_featured": True,
                "stream_url": "https://demo.unified-streaming.com/k8s/features/stable/video/tears-of-steel/tears-of-steel.ism/.m3u8",
                # Add realistic betting odds
                "home_odds": 2.10,
                "away_odds": 3.40,
                "draw_odds": 3.20
            }
            
            new_match = Match(**match_data)
            db.add(new_match)
            
            print(f"✅ Added: {match_data['title']}")
        
        # Also add a few more realistic matches for today
        other_matches = [
            {
                "external_id": 999998,
                "title": "Barcelona vs Liverpool",
                "home_team": "Barcelona",
                "away_team": "Liverpool",
                "home_score": 1 if datetime.now().hour >= 20 else 0,
                "away_score": 0 if datetime.now().hour >= 20 else 0,
                "status": MatchStatus.LIVE if datetime.now().hour >= 20 else MatchStatus.SCHEDULED,
                "scheduled_at": datetime.now().replace(hour=20, minute=0, second=0, microsecond=0),
                "is_featured": True,
                "stream_url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8",
                "home_odds": 1.85,
                "away_odds": 4.20,
                "draw_odds": 3.60
            },
            {
                "external_id": 999997,
                "title": "Arsenal vs Bayern Munich",
                "home_team": "Arsenal",
                "away_team": "Bayern Munich",
                "home_score": 0,
                "away_score": 0,
                "status": MatchStatus.SCHEDULED,
                "scheduled_at": datetime.now().replace(hour=22, minute=30, second=0, microsecond=0),
                "is_featured": True,
                "stream_url": "https://bitdash-a.akamaihd.net/content/sintel/hls/playlist.m3u8",
                "home_odds": 2.75,
                "away_odds": 2.60,
                "draw_odds": 3.10
            }
        ]
        
        for match_data in other_matches:
            existing = db.query(Match).filter(
                Match.home_team == match_data["home_team"],
                Match.away_team == match_data["away_team"]
            ).first()
            
            if not existing:
                new_match = Match(**match_data)
                db.add(new_match)
                print(f"✅ Added: {match_data['title']}")
        
        db.commit()
        
        # Show summary
        live_count = db.query(Match).filter(Match.status == MatchStatus.LIVE).count()
        scheduled_today = db.query(Match).filter(
            Match.scheduled_at >= datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
            Match.scheduled_at < datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        ).count()
        
        print(f"\n📊 Match Summary:")
        print(f"   • Live matches: {live_count}")
        print(f"   • Scheduled today: {scheduled_today}")
        
        print(f"\n🎬 How to Watch:")
        print(f"   1. Visit: http://localhost:3000/dashboard")
        print(f"   2. Click '🔴 Live' to see live matches")
        print(f"   3. Click 'All Leagues' to see all matches")
        print(f"   4. Look for 'Real Madrid vs Manchester City'!")
        
        print(f"\n⏰ Match Schedule:")
        print(f"   • Barcelona vs Liverpool: 8:00 PM")
        print(f"   • Real Madrid vs Manchester City: 9:00 PM")
        print(f"   • Arsenal vs Bayern Munich: 10:30 PM")
        
        current_hour = datetime.now().hour
        if current_hour >= 21:
            print(f"\n🔴 Real Madrid vs Manchester City is LIVE NOW!")
        elif current_hour >= 20:
            print(f"\n🔴 Barcelona vs Liverpool is LIVE NOW!")
            print(f"⏰ Real Madrid vs Manchester City starts in {21 - current_hour} hour(s)")
        else:
            print(f"\n⏰ First match starts at 8:00 PM ({20 - current_hour} hour(s) from now)")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_real_madrid_city_match()