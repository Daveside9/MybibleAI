#!/usr/bin/env python3
"""
Verify Clean Database - Check that only real matches remain
"""

from app.core.database import get_db
from app.models.match import Match
from sqlalchemy import or_

def verify_clean_database():
    """Verify that database contains only real matches"""
    
    db = next(get_db())
    
    try:
        print('🔍 Verifying database cleanliness...')
        
        # Count total matches
        total_matches = db.query(Match).count()
        print(f'   Total matches in database: {total_matches}')
        
        # Count real matches (external_id > 0)
        real_matches = db.query(Match).filter(Match.external_id > 0).count()
        print(f'   Real matches (external_id > 0): {real_matches}')
        
        # Check for any remaining mock matches
        mock_matches = db.query(Match).filter(
            or_(
                Match.external_id.between(999000, 999999),
                Match.stream_url.like('%demo%'),
                Match.stream_url.like('%test%'),
                Match.stream_url.like('%bitdash%'),
                Match.external_id.is_(None),
                Match.external_id == 0
            )
        ).count()
        print(f'   Mock matches remaining: {mock_matches}')
        
        # Check matches by league
        from app.models.match import League
        from sqlalchemy import func
        leagues_with_matches = db.query(League.name, func.count(Match.id).label('count')).join(
            Match, Match.league_id == League.id
        ).group_by(League.name).order_by(func.count(Match.id).desc()).all()
        
        print(f'\n📊 Matches by league:')
        for league_name, count in leagues_with_matches[:10]:
            print(f'   {league_name}: {count} matches')
        
        if len(leagues_with_matches) > 10:
            print(f'   ... and {len(leagues_with_matches) - 10} more leagues')
        
        # Check featured matches
        featured_matches = db.query(Match).filter(Match.is_featured == True).count()
        print(f'\n⭐ Featured matches: {featured_matches}')
        
        # Sample some matches to verify they look real
        sample_matches = db.query(Match).filter(Match.external_id > 0).limit(5).all()
        print(f'\n🏈 Sample real matches:')
        for i, match in enumerate(sample_matches, 1):
            league_name = match.league.name if match.league else 'No League'
            print(f'   {i}. {match.home_team} vs {match.away_team} | League: {league_name} | External ID: {match.external_id}')
        
        # Final verification
        if mock_matches == 0 and real_matches == total_matches:
            print(f'\n✅ Database is clean!')
            print(f'   All {total_matches} matches are real with valid external IDs')
            print(f'   No mock/test matches remain')
            return True
        else:
            print(f'\n⚠️  Database may still have issues:')
            print(f'   Total: {total_matches}, Real: {real_matches}, Mock: {mock_matches}')
            return False
            
    except Exception as e:
        print(f'❌ Error during verification: {e}')
        return False
    finally:
        db.close()

if __name__ == "__main__":
    verify_clean_database()