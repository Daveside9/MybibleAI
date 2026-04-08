#!/usr/bin/env python3
"""
Find Sporting CP Match - Find the live Sporting CP match
"""

from app.core.database import get_db
from app.models.match import Match, MatchStatus

def find_sporting_cp_match():
    """Find the Sporting CP match that's currently live"""
    
    db = next(get_db())
    
    try:
        print('🔍 Searching for Sporting CP matches...')
        
        # Search for Sporting CP matches (various name variations)
        sporting_variations = [
            'Sporting CP',
            'Sporting',
            'Sporting Lisbon',
            'Sporting Lisboa'
        ]
        
        all_matches = []
        
        for variation in sporting_variations:
            # Search in home team
            home_matches = db.query(Match).filter(
                Match.home_team.ilike(f'%{variation}%')
            ).all()
            
            # Search in away team
            away_matches = db.query(Match).filter(
                Match.away_team.ilike(f'%{variation}%')
            ).all()
            
            all_matches.extend(home_matches)
            all_matches.extend(away_matches)
        
        # Remove duplicates
        unique_matches = list({match.id: match for match in all_matches}.values())
        
        if not unique_matches:
            print('❌ No Sporting CP matches found!')
            return
        
        print(f'✅ Found {len(unique_matches)} Sporting CP matches:')
        
        live_matches = []
        scheduled_matches = []
        
        for match in unique_matches:
            print(f'   ID: {match.id}')
            print(f'   Match: {match.home_team} vs {match.away_team}')
            print(f'   Status: {match.status.value}')
            print(f'   Scheduled: {match.scheduled_at}')
            print(f'   Stream URL: {match.stream_url}')
            print(f'   External ID: {match.external_id}')
            print()
            
            if match.status == MatchStatus.LIVE:
                live_matches.append(match)
            elif match.status == MatchStatus.SCHEDULED:
                scheduled_matches.append(match)
        
        if live_matches:
            print(f'🔴 Found {len(live_matches)} LIVE Sporting CP matches:')
            for match in live_matches:
                print(f'   🔴 ID {match.id}: {match.home_team} vs {match.away_team}')
        
        if scheduled_matches:
            print(f'⏰ Found {len(scheduled_matches)} scheduled Sporting CP matches:')
            for match in scheduled_matches:
                print(f'   ⏰ ID {match.id}: {match.home_team} vs {match.away_team}')
        
        # If no live matches, let's set one to live for testing
        if not live_matches and unique_matches:
            print(f'\n💡 No live matches found. Setting the first match to LIVE for testing...')
            test_match = unique_matches[0]
            test_match.status = MatchStatus.LIVE
            db.commit()
            print(f'✅ Set match ID {test_match.id} to LIVE: {test_match.home_team} vs {test_match.away_team}')
            return test_match.id
        elif live_matches:
            return live_matches[0].id
        
        return None
        
    except Exception as e:
        print(f'❌ Error finding Sporting CP match: {e}')
        db.rollback()
        return None
    finally:
        db.close()

if __name__ == "__main__":
    match_id = find_sporting_cp_match()
    if match_id:
        print(f'\n🎯 Use match ID {match_id} for live streaming test!')