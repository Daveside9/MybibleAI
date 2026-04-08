#!/usr/bin/env python3
"""
Show Working Match URLs - Display valid match URLs for testing
"""

from app.core.database import get_db
from app.models.match import Match

def show_working_match_urls():
    """Show working match URLs for testing streaming"""
    
    db = next(get_db())
    
    try:
        print('🎯 Working Match URLs for Testing Streaming:')
        print('=' * 60)
        
        # Get some live or scheduled matches
        live_matches = db.query(Match).filter(
            Match.status == 'live',
            Match.external_id > 0
        ).limit(5).all()
        
        scheduled_matches = db.query(Match).filter(
            Match.status == 'scheduled',
            Match.external_id > 0
        ).limit(10).all()
        
        if live_matches:
            print(f'\n🔴 LIVE MATCHES (Ready for streaming):')
            for i, match in enumerate(live_matches, 1):
                league_name = match.league.name if match.league else 'No League'
                print(f'   {i}. http://localhost:3000/match/{match.id}')
                print(f'      {match.home_team} vs {match.away_team}')
                print(f'      League: {league_name} | Status: {match.status.value.upper()}')
                print()
        else:
            print(f'\n🔴 No live matches currently available')
        
        print(f'\n⏰ UPCOMING MATCHES (Available for streaming):')
        for i, match in enumerate(scheduled_matches, 1):
            league_name = match.league.name if match.league else 'No League'
            print(f'   {i}. http://localhost:3000/match/{match.id}')
            print(f'      {match.home_team} vs {match.away_team}')
            print(f'      League: {league_name} | Status: {match.status.value.upper()}')
            if i >= 5:  # Limit to 5 for readability
                break
        
        if len(scheduled_matches) > 5:
            print(f'   ... and {len(scheduled_matches) - 5} more scheduled matches')
        
        print(f'\n💡 How to test streaming:')
        print(f'   1. Copy any URL above')
        print(f'   2. Paste it in your browser')
        print(f'   3. The match page should load without "Failed to fetch" error')
        print(f'   4. You can test the video player and chat functionality')
        
        print(f'\n⚠️  URLs to AVOID (these will cause "Failed to fetch"):')
        print(f'   - http://localhost:3000/match/1 to /match/5')
        print(f'   - http://localhost:3000/match/83')
        print(f'   - http://localhost:3000/match/197 to /match/226')
        print(f'   - Any other missing ID from the deleted mock matches')
        
    except Exception as e:
        print(f'❌ Error showing working URLs: {e}')
    finally:
        db.close()

if __name__ == "__main__":
    show_working_match_urls()