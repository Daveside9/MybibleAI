#!/usr/bin/env python3
"""
Prioritize Real Matches in Dashboard
Make real matches show up first by updating their scheduled times and featured status
"""
import sys
import os
from datetime import datetime, date, timedelta

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.match import Match, MatchStatus

def prioritize_real_matches():
    """Make real matches show up first in dashboard"""
    
    db = SessionLocal()
    
    try:
        print("🎯 Prioritizing Real Matches for Dashboard...")
        print("=" * 50)
        
        # Get today's date
        today = date.today()
        now = datetime.now()
        
        # Find real matches (those with external_id > 0)
        real_matches = db.query(Match).filter(
            Match.external_id > 0
        ).all()
        
        print(f"📊 Found {len(real_matches)} real matches")
        
        # Update real matches to be featured and scheduled for today
        updated_count = 0
        for match in real_matches:
            # Make it featured
            match.is_featured = True
            
            # If it's not scheduled for today, move it to today
            if match.scheduled_at.date() != today:
                # Schedule it for today at various times
                hour = 12 + (updated_count % 10)  # Spread between 12:00 and 21:00
                minute = (updated_count * 15) % 60  # Different minutes
                
                new_time = datetime.combine(today, datetime.min.time().replace(hour=hour, minute=minute))
                match.scheduled_at = new_time
                
                print(f"📅 Moved to today: {match.title} -> {new_time.strftime('%H:%M')}")
            
            # Make some matches live for demo
            if updated_count < 5:  # First 5 matches are live
                match.status = MatchStatus.LIVE
                match.started_at = now - timedelta(minutes=updated_count * 10)
                print(f"🔴 Made LIVE: {match.title}")
            
            updated_count += 1
        
        # Unfeatured old mock matches (those with external_id = 0 or None)
        mock_matches = db.query(Match).filter(
            (Match.external_id == 0) | (Match.external_id == None)
        ).all()
        
        unfeatured_count = 0
        for match in mock_matches:
            if match.is_featured:
                match.is_featured = False
                unfeatured_count += 1
                print(f"⭐ Unfeatured mock: {match.title}")
        
        # Commit changes
        db.commit()
        
        print(f"\n✅ Dashboard Prioritization Complete!")
        print(f"   • Updated {updated_count} real matches")
        print(f"   • Unfeatured {unfeatured_count} mock matches")
        print(f"   • Made 5 matches LIVE for demo")
        
        # Show current status
        live_count = db.query(Match).filter(Match.status == MatchStatus.LIVE).count()
        featured_count = db.query(Match).filter(Match.is_featured == True).count()
        today_start = datetime.combine(today, datetime.min.time())
        today_end = datetime.combine(today, datetime.max.time())
        today_count = db.query(Match).filter(
            Match.scheduled_at >= today_start,
            Match.scheduled_at <= today_end,
            Match.is_featured == True
        ).count()
        
        print(f"\n📊 Current Status:")
        print(f"   • Live matches: {live_count}")
        print(f"   • Featured matches: {featured_count}")
        print(f"   • Today's featured matches: {today_count}")
        
        # Show today's featured matches
        print(f"\n🎯 Today's Featured Matches (First 10):")
        todays_featured = db.query(Match).filter(
            Match.scheduled_at >= today_start,
            Match.scheduled_at <= today_end,
            Match.is_featured == True
        ).order_by(Match.scheduled_at).limit(10).all()
        
        for match in todays_featured:
            status_icon = "🔴" if match.status == MatchStatus.LIVE else "⏰"
            time_str = match.scheduled_at.strftime('%H:%M')
            print(f"   {status_icon} {time_str} - {match.title}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = prioritize_real_matches()
    
    if success:
        print(f"\n🎬 Next Steps:")
        print(f"   1. Refresh your dashboard: http://localhost:3000/dashboard")
        print(f"   2. You should now see real matches like:")
        print(f"      • Celtic vs AS Roma")
        print(f"      • FC Basel vs Aston Villa") 
        print(f"      • Dinamo Zagreb vs Real Betis")
        print(f"   3. Click '🔴 Live' to see 5 live matches")
        print(f"   4. All real matches are now featured and scheduled for today!")
    else:
        print(f"\n💥 Failed to prioritize matches")