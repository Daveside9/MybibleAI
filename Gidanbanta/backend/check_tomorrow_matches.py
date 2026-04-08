#!/usr/bin/env python3
"""
Check matches for tomorrow to identify mock matches
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import get_db
from app.models.match import Match
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

def check_tomorrow_matches():
    """Check matches for tomorrow and identify potential mock matches"""
    
    # Get database session
    db = next(get_db())
    
    try:
        # Get tomorrow's date
        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow_start = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow_end = tomorrow.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        print(f'Checking matches for tomorrow: {tomorrow_start.date()}')
        print('=' * 50)
        
        # Query matches for tomorrow
        matches = db.query(Match).filter(
            Match.scheduled_at >= tomorrow_start,
            Match.scheduled_at <= tomorrow_end
        ).order_by(Match.scheduled_at).all()
        
        print(f'Total matches found for tomorrow: {len(matches)}')
        print()
        
        # Current mock match filter list
        current_mock_names = [
            "Liverpool vs Chelsea",
            "Toulouse vs Eintracht Frankfurt", 
            "Chelsea vs Atletico Madrid",
            "Toulouse vs Slavia Prague",
            "Ajax vs PAOK",
            "Bologna vs Fiorentina",
            "Fulham vs Bournemouth",
            "Athletic Bilbao vs Sevilla"
        ]
        
        real_matches = []
        potential_mocks = []
        filtered_mocks = []
        
        for match in matches:
            print(f'Match: {match.title}')
            print(f'  External ID: {match.external_id}')
            print(f'  League ID: {match.league_id}')
            print(f'  Scheduled: {match.scheduled_at}')
            print(f'  Featured: {match.is_featured}')
            
            # Check if this is already filtered
            if match.title in current_mock_names:
                filtered_mocks.append(match.title)
                print(f'  Status: FILTERED (already in mock list)')
            # Check if this looks like a mock match (no external_id or external_id = 0)
            elif match.external_id is None or match.external_id == 0:
                potential_mocks.append(match.title)
                print(f'  Status: POTENTIAL MOCK (no external_id)')
            else:
                real_matches.append(match.title)
                print(f'  Status: REAL MATCH')
            
            print()
        
        print('SUMMARY:')
        print('=' * 50)
        print(f'Real matches: {len(real_matches)}')
        print(f'Already filtered mocks: {len(filtered_mocks)}')
        print(f'Potential new mocks: {len(potential_mocks)}')
        
        if potential_mocks:
            print('\nPOTENTIAL MOCK MATCHES TO ADD TO FILTER:')
            for mock in potential_mocks:
                print(f'  - "{mock}"')
        
        if filtered_mocks:
            print('\nALREADY FILTERED MOCK MATCHES:')
            for mock in filtered_mocks:
                print(f'  - "{mock}"')
        
        if real_matches:
            print('\nREAL MATCHES:')
            for real in real_matches[:5]:  # Show first 5
                print(f'  - "{real}"')
            if len(real_matches) > 5:
                print(f'  ... and {len(real_matches) - 5} more')
        
    finally:
        db.close()

if __name__ == "__main__":
    check_tomorrow_matches()