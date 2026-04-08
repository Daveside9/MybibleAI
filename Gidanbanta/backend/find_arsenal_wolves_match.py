#!/usr/bin/env python3
"""
Find Arsenal vs Wolves Match - Locate the specific match you're trying to stream
"""

from app.core.database import get_db
from app.models.match import Match
from sqlalchemy import or_

def find_arsenal_wolves_match():
    """Find the Arsenal vs Wolverhampton match"""
    
    db = next(get_db())
    
    try:
        print('🔍 Searching for Arsenal vs Wolverhampton match...')
        
        # Search for Arsenal vs Wolves variations
        arsenal_wolves_matches = db.query(Match).filter(
            or_(
                # Arsenal as home team
                (Match.home_team.like('%Arsenal%')) & (Match.away_team.like('%Wol%')),
                # Arsenal as away team  
                (Match.away_team.like('%Arsenal%')) & (Match.home_team.like('%Wol%')),
                # Alternative spellings
                (Match.home_team.like('%Arsenal%')) & (Match.away_team.like('%Wolverhampton%')),
                (Match.away_team.like('%Arsenal%')) & (Match.home_team.like('%Wolverhampton%'))
            )
        ).all()
        
        if arsenal_wolves_matches:
            print(f'✅ Found {len(arsenal_wolves_matches)} Arsenal vs Wolves matches:')
            for i, match in enumerate(arsenal_wolves_matches, 1):
                league_name = match.league.name if match.league else 'No League'
                status_emoji = '🔴' if match.status.value == 'live' else '⏰' if match.status.value == 'scheduled' else '🏁'
                
                print(f'\n   {i}. Match ID: {match.id}')
                print(f'      {status_emoji} {match.home_team} vs {match.away_team}')
                print(f'      Status: {match.status.value.upper()}')
                print(f'      League: {league_name}')
                print(f'      Scheduled: {match.scheduled_at}')
                print(f'      External ID: {match.external_id}')
                print(f'      URL: http://localhost:3000/match/{match.id}')
                
                if match.status.value == 'live':
                    print(f'      🎯 THIS IS LIVE - Use this URL to stream!')
        else:
            print('❌ No Arsenal vs Wolverhampton matches found')
            
            # Let's search for just Arsenal matches
            print('\n🔍 Searching for any Arsenal matches...')
            arsenal_matches = db.query(Match).filter(
                or_(
                    Match.home_team.like('%Arsenal%'),
                    Match.away_team.like('%Arsenal%')
                )
            ).limit(5).all()
            
            if arsenal_matches:
                print(f'   Found {len(arsenal_matches)} Arsenal matches:')
                for match in arsenal_matches:
                    status_emoji = '🔴' if match.status.value == 'live' else '⏰' if match.status.value == 'scheduled' else '🏁'
                    print(f'   {status_emoji} ID {match.id}: {match.home_team} vs {match.away_team} | {match.status.value.upper()}')
            
            # Let's search for Wolves matches
            print('\n🔍 Searching for any Wolves/Wolverhampton matches...')
            wolves_matches = db.query(Match).filter(
                or_(
                    Match.home_team.like('%Wol%'),
                    Match.away_team.like('%Wol%')
                )
            ).limit(5).all()
            
            if wolves_matches:
                print(f'   Found {len(wolves_matches)} Wolves matches:')
                for match in wolves_matches:
                    status_emoji = '🔴' if match.status.value == 'live' else '⏰' if match.status.value == 'scheduled' else '🏁'
                    print(f'   {status_emoji} ID {match.id}: {match.home_team} vs {match.away_team} | {match.status.value.upper()}')
        
        # Also check for any live matches currently
        print('\n🔴 All currently LIVE matches:')
        live_matches = db.query(Match).filter(Match.status == 'live').all()
        
        if live_matches:
            for match in live_matches:
                league_name = match.league.name if match.league else 'No League'
                print(f'   🔴 ID {match.id}: {match.home_team} vs {match.away_team}')
                print(f'      League: {league_name} | URL: http://localhost:3000/match/{match.id}')
        else:
            print('   No matches are currently marked as LIVE in the database')
        
    except Exception as e:
        print(f'❌ Error searching for Arsenal vs Wolves: {e}')
    finally:
        db.close()

if __name__ == "__main__":
    find_arsenal_wolves_match()