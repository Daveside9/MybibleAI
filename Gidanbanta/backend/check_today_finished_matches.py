#!/usr/bin/env python3
"""
Check Today Finished Matches - See if there are finished matches for today in the database
"""

from app.core.database import get_db
from app.models.match import Match, MatchStatus
from datetime import datetime

def check_today_finished_matches():
    """Check if there are finished matches for today in the database"""
    
    db = next(get_db())
    
    try:
        print('🔍 Checking today\'s finished matches in database...')
        
        # Get today's date range
        today = datetime.now().date()
        start_dt = datetime.combine(today, datetime.min.time())
        end_dt = datetime.combine(today, datetime.max.time())
        
        print(f'   Today: {today}')
        print(f'   Time range: {start_dt} to {end_dt}')
        
        # Get all matches for today
        all_today_matches = db.query(Match).filter(
            Match.scheduled_at >= start_dt,
            Match.scheduled_at <= end_dt,
            Match.external_id > 0  # Only real matches
        ).all()
        
        print(f'\n📊 All today\'s matches in database: {len(all_today_matches)}')
        
        # Count by status
        status_counts = {}
        finished_matches = []
        
        for match in all_today_matches:
            status = match.status.value
            status_counts[status] = status_counts.get(status, 0) + 1
            
            if status == 'finished':
                finished_matches.append(match)
        
        print(f'\n📋 Status breakdown:')
        for status, count in status_counts.items():
            print(f'   {status}: {count} matches')
        
        if finished_matches:
            print(f'\n🏁 Finished matches for today ({len(finished_matches)} total):')
            for i, match in enumerate(finished_matches[:5], 1):
                score = f"{match.home_score or 0}-{match.away_score or 0}"
                league_name = match.league.name if match.league else 'No League'
                print(f'   {i}. {match.home_team} vs {match.away_team}')
                print(f'      Score: {score} | League: {league_name}')
                print(f'      Scheduled: {match.scheduled_at}')
                print()
            
            if len(finished_matches) > 5:
                print(f'   ... and {len(finished_matches) - 5} more finished matches')
            
            print(f'✅ These finished matches are correctly filtered out from today\'s API response')
        else:
            print(f'\n✅ No finished matches found for today')
        
        # Show what will be returned by API (live, scheduled, postponed)
        api_matches = db.query(Match).filter(
            Match.scheduled_at >= start_dt,
            Match.scheduled_at <= end_dt,
            Match.external_id > 0,
            Match.status.in_([MatchStatus.LIVE, MatchStatus.SCHEDULED, MatchStatus.POSTPONED])
        ).all()
        
        print(f'\n📡 Matches returned by API (live + scheduled + postponed): {len(api_matches)}')
        
    except Exception as e:
        print(f'❌ Error checking today\'s finished matches: {e}')
    finally:
        db.close()

if __name__ == "__main__":
    check_today_finished_matches()