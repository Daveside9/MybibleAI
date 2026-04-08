#!/usr/bin/env python3
"""
Check Current Matches - See what matches are actually showing up
"""

from app.core.database import get_db
from app.models.match import Match
from sqlalchemy import or_
from datetime import datetime, timedelta

def check_current_matches():
    """Check what matches are currently in the database and showing"""
    
    db = next(get_db())
    
    try:
        print('🔍 Checking current matches in database...')
        
        # Get today's date
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)
        
        print(f'   Today: {today}')
        print(f'   Tomorrow: {tomorrow}')
        
        # Check matches for today
        today_matches = db.query(Match).filter(
            Match.scheduled_at >= datetime.combine(today, datetime.min.time()),
            Match.scheduled_at < datetime.combine(tomorrow, datetime.min.time())
        ).all()
        
        print(f'\n📅 Today\'s matches ({len(today_matches)} total):')
        for i, match in enumerate(today_matches[:10], 1):
            external_id = match.external_id or 'None'
            home_score = match.home_score if match.home_score is not None else '-'
            away_score = match.away_score if match.away_score is not None else '-'
            score_display = f"{home_score}-{away_score}" if match.home_score is not None or match.away_score is not None else "No Score"
            league_name = match.league.name if match.league else 'No League'
            
            print(f'   {i}. {match.home_team} vs {match.away_team}')
            print(f'      League: {league_name} | External ID: {external_id}')
            print(f'      Score: {score_display} | Status: {match.status.value}')
            print(f'      Scheduled: {match.scheduled_at}')
            print()
        
        if len(today_matches) > 10:
            print(f'   ... and {len(today_matches) - 10} more matches')
        
        # Check for matches with scores that shouldn't have them
        future_matches_with_scores = db.query(Match).filter(
            Match.scheduled_at > datetime.now(),
            or_(Match.home_score.isnot(None), Match.away_score.isnot(None))
        ).all()
        
        if future_matches_with_scores:
            print(f'\n⚠️  Found {len(future_matches_with_scores)} future matches with scores (these might be the issue):')
            for i, match in enumerate(future_matches_with_scores[:5], 1):
                score = f"{match.home_score or 0}-{match.away_score or 0}"
                print(f'   {i}. {match.home_team} vs {match.away_team} | Score: {score} | Scheduled: {match.scheduled_at}')
        
        # Check for any remaining suspicious matches
        suspicious_matches = db.query(Match).filter(
            or_(
                Match.external_id.between(999000, 999999),
                Match.stream_url.like('%demo%'),
                Match.stream_url.like('%test%'),
                Match.stream_url.like('%bitdash%'),
                Match.external_id.is_(None),
                Match.external_id == 0
            )
        ).all()
        
        if suspicious_matches:
            print(f'\n❌ Found {len(suspicious_matches)} suspicious matches still in database:')
            for i, match in enumerate(suspicious_matches, 1):
                external_id = match.external_id or 'None'
                stream_info = 'Demo/Test Stream' if match.stream_url and ('demo' in match.stream_url or 'test' in match.stream_url) else 'Regular'
                print(f'   {i}. {match.home_team} vs {match.away_team} | External ID: {external_id} | {stream_info}')
        else:
            print(f'\n✅ No suspicious matches found in database')
        
        # Check featured matches
        featured_matches = db.query(Match).filter(Match.is_featured == True).all()
        print(f'\n⭐ Featured matches: {len(featured_matches)}')
        for i, match in enumerate(featured_matches[:5], 1):
            score = f"{match.home_score or 0}-{match.away_score or 0}" if match.home_score is not None or match.away_score is not None else "No Score"
            print(f'   {i}. {match.home_team} vs {match.away_team} | Score: {score} | Status: {match.status.value}')
        
    except Exception as e:
        print(f'❌ Error checking matches: {e}')
    finally:
        db.close()

if __name__ == "__main__":
    check_current_matches()