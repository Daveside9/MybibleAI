#!/usr/bin/env python3
"""
Check Match Database - Verify the Arsenal match exists and has stream URL
"""

from app.core.database import get_db
from app.models.match import Match

def check_match_database():
    """Check if Arsenal vs Wolves match exists in database"""
    
    db = next(get_db())
    
    try:
        print('🔍 Checking Arsenal vs Wolves match in database...')
        
        # Find the Arsenal vs Wolves match
        match = db.query(Match).filter(Match.id == 230).first()
        
        if not match:
            print('❌ Match ID 230 not found in database!')
            
            # Check if there are any Arsenal matches
            arsenal_matches = db.query(Match).filter(
                Match.home_team.ilike('%arsenal%') | 
                Match.away_team.ilike('%arsenal%')
            ).all()
            
     