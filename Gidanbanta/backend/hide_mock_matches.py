#!/usr/bin/env python3
"""
Hide Mock Matches - Make mock matches not featured so they don't show in dashboard
"""
import sys
import os

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.match import Match

def hide_mock_matches():
    """Hide mock matches by setting is_featured=False for matches without external_id"""
    
    db = SessionLocal()
    
    try:
        print("🚫 Hiding Mock Matches from Dashboard...")
        print("=" * 50)
        
        # Find mock matches (external_id is 0 or None)
        mock_matches = db.query(Match).filter(
            (Match.external_id == 0) | (Match.external_id == None)
        ).all()
        
        print(f"📊 Found {len(mock_matches)} mock matches")
        
        # Hide mock matches by setting is_featured=False
        hidden_count = 0
        for match in mock_matches:
            if match.is_featured:
                match.is_featured = False
                hidden_count += 1
                print(f"🚫 Hidden: {match.title}")
        
        # Commit changes
        db.commit()
        
        print(f"\n✅ Mock Matches Hidden!")
        print(f"   • Hidden {hidden_count} mock matches")
        print(f"   • Mock matches will no longer appear in dashboard")
        
        # Show current status
        real_matches = db.query(Match).filter(
            Match.external_id > 0,
            Match.is_featured == True
        ).count()
        
        mock_matches_visible = db.query(Match).filter(
            (Match.external_id == 0) | (Match.external_id == None),
            Match.is_featured == True
        ).count()
        
        print(f"\n📊 Current Status:")
        print(f"   • Real matches (featured): {real_matches}")
        print(f"   • Mock matches (featured): {mock_matches_visible}")
        
        if mock_matches_visible == 0:
            print(f"   🎉 All mock matches are now hidden!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = hide_mock_matches()
    
    if success:
        print(f"\n🎬 Next Steps:")
        print(f"   1. Refresh your dashboard: http://localhost:3000/dashboard")
        print(f"   2. You should now see ONLY real matches:")
        print(f"      • Celtic vs AS Roma")
        print(f"      • FC Basel vs Aston Villa") 
        print(f"      • Dinamo Zagreb vs Real Betis")
        print(f"      • And other Europa League matches")
        print(f"   3. No more Liverpool vs Chelsea or other mock matches!")
    else:
        print(f"\n💥 Failed to hide mock matches")