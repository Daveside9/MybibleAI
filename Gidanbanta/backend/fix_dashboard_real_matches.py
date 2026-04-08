#!/usr/bin/env python3
"""
Fix Dashboard to Show Only Real Matches
Remove old mock matches and ensure real matches are featured
"""
import sys
import os
from datetime import datetime, date

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.match import Match, MatchStatus

def fix_dashboard_matches():
    """Remove old mock matches and ensure real matches are featured"""
    
    db = SessionLocal()
    
    try:
        print("🔧 Fixing Dashboard Matches...")
        print("=" * 50)
        
        # List of old mock matches to remove
        mock_matches = [
            "Liverpool vs Chelsea",
            "Toulouse vs Eintracht Frankfurt", 
            "Chelsea vs Atletico Madrid",
            "Toulouse vs Slavia Prague",
            "Ajax vs PAOK",
            "Bologna vs Fiorentina",
            "Fulham vs Bournemouth",
            "Athletic Bilbao vs Sevilla"
        ]
        
        # Remove old mock matches
        removed_count = 0
        for mock_title in mock_matches:
            mock_match = db.query(Match).filter(Match.title == mock_title).first()
            if mock_match:
                print(f"❌ Removing mock match: {mock_title}")
                db.delete(mock_match)
                removed_count += 1
        
        # Make sure all real matches from today are featured
        today = date.today()
        today_start = datetime.combine(today, datetime.min.time())
        today_end = datetime.combine(today, datetime.max.time())
        
        real_matches = db.query(Match).filter(
            Match.scheduled_at >= today_start,
            Match.scheduled_at <= today_end,
            Match.external_id > 0  # Real matches have external IDs
        ).all()
        
        featured_count = 0
        for match in real_matches:
            if not match.is_featured:
                match.is_featured = True
                featured_count += 1
                print(f"⭐ Making featured: {match.title}")
        
        # Commit changes
        db.commit()
        
        print(f"\n✅ Dashboard Fixed!")
        print(f"   • Removed {removed_count} mock matches")
        print(f"   • Made {featured_count} real matches featured")
        
        # Show current status
        live_count = db.query(Match).filter(Match.status == MatchStatus.LIVE).count()
        featured_count = db.query(Match).filter(Match.is_featured == True).count()
        today_count = db.query(Match).filter(
            Match.scheduled_at >= today_start,
            Match.scheduled_at <= today_end
        ).count()
        
        print(f"\n📊 Current Status:")
        print(f"   • Live matches: {live_count}")
        print(f"   • Featured matches: {featured_count}")
        print(f"   • Today's matches: {today_count}")
        
        # Show today's featured matches
        print(f"\n🎯 Today's Featured Matches:")
        todays_featured = db.query(Match).filter(
            Match.scheduled_at >= today_start,
            Match.scheduled_at <= today_end,
            Match.is_featured == True
        ).order_by(Match.scheduled_at).limit(10).all()
        
        for match in todays_featured:
            status_icon = "🔴" if match.status == MatchStatus.LIVE else "⏰"
            print(f"   {status_icon} {match.title} - {match.status.value}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = fix_dashboard_matches()
    
    if success:
        print(f"\n🎬 Next Steps:")
        print(f"   1. Refresh your dashboard: http://localhost:3000/dashboard")
        print(f"   2. You should now see real matches like:")
        print(f"      • Celtic vs AS Roma")
        print(f"      • FC Basel vs Aston Villa") 
        print(f"      • Dinamo Zagreb vs Real Betis")
        print(f"   3. Click '🔴 Live' to see live matches")
    else:
        print(f"\n💥 Failed to fix dashboard")