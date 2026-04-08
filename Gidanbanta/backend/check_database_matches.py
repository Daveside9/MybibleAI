#!/usr/bin/env python3
"""
Check what matches are currently in the database
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.match import Match, MatchStatus
from datetime import datetime, date

def check_database_matches():
    """Check what matches are in the database"""
    
    print("🔍 Checking Database Matches")
    print("=" * 50)
    
    db = SessionLocal()
    
    try:
        # Get all matches
        all_matches = db.query(Match).all()
        print(f"📊 Total matches in database: {len(all_matches)}")
        
        if not all_matches:
            print("❌ No matches found in database!")
            return
        
        # Group by status
        live_matches = db.query(Match).filter(Match.status == MatchStatus.LIVE).all()
        scheduled_matches = db.query(Match).filter(Match.status == MatchStatus.SCHEDULED).all()
        featured_matches = db.query(Match).filter(Match.is_featured == True).all()
        
        print(f"🔴 Live matches: {len(live_matches)}")
        print(f"⏰ Scheduled matches: {len(scheduled_matches)}")
        print(f"⭐ Featured matches: {len(featured_matches)}")
        
        # Show recent matches
        print(f"\n📋 Recent Matches:")
        print("-" * 60)
        
        recent_matches = db.query(Match).order_by(Match.created_at.desc()).limit(10).all()
        
        for match in recent_matches:
            status_icon = "🔴" if match.status == MatchStatus.LIVE else "⏰" if match.status == MatchStatus.SCHEDULED else "✅"
            featured_icon = "⭐" if match.is_featured else "  "
            
            print(f"{status_icon}{featured_icon} {match.title}")
            print(f"     Score: {match.home_score} - {match.away_score}")
            print(f"     Status: {match.status}")
            print(f"     Featured: {match.is_featured}")
            print(f"     Scheduled: {match.scheduled_at}")
            print(f"     Stream: {'Yes' if match.stream_url else 'No'}")
            print()
        
        # Check for specific matches
        print(f"🔍 Looking for specific matches:")
        
        real_madrid_matches = db.query(Match).filter(
            (Match.home_team.like('%Real Madrid%')) | 
            (Match.away_team.like('%Real Madrid%'))
        ).all()
        
        city_matches = db.query(Match).filter(
            (Match.home_team.like('%Manchester City%')) | 
            (Match.away_team.like('%Manchester City%')) |
            (Match.home_team.like('%City%')) | 
            (Match.away_team.like('%City%'))
        ).all()
        
        print(f"   Real Madrid matches: {len(real_madrid_matches)}")
        print(f"   Manchester City matches: {len(city_matches)}")
        
        for match in real_madrid_matches:
            print(f"   ⚽ {match.title} - {match.status} - Featured: {match.is_featured}")
        
        for match in city_matches:
            print(f"   ⚽ {match.title} - {match.status} - Featured: {match.is_featured}")
        
        # Check today's matches
        today = date.today()
        today_matches = db.query(Match).filter(
            Match.scheduled_at >= datetime.combine(today, datetime.min.time()),
            Match.scheduled_at < datetime.combine(today, datetime.max.time())
        ).all()
        
        print(f"\n📅 Today's matches: {len(today_matches)}")
        for match in today_matches:
            print(f"   {match.title} at {match.scheduled_at.strftime('%H:%M')}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_database_matches()