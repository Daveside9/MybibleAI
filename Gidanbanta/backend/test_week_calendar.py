#!/usr/bin/env python3
"""
Test Calendar Sync Across Multiple Days
"""
import requests
from datetime import datetime, timedelta

def test_week_calendar():
    """Test calendar across a week"""
    
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0IiwiZXhwIjoxNzY1NTQxNzU1LCJ0eXBlIjoiYWNjZXNzIn0.1Ve4VRlenOoThwEAJmW3Ls1lfJmpQ-jdyV0tRk7hmt0'
    headers = {'Authorization': f'Bearer {token}'}
    
    print('📅 Testing calendar sync across multiple dates...')
    
    total_matches = 0
    
    for i in range(7):
        date = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')
        try:
            response = requests.get(
                f'http://localhost:4000/v1/matches/calendar/matches?start_date={date}&end_date={date}',
                headers=headers
            )
            if response.status_code == 200:
                data = response.json()
                day_name = (datetime.now() + timedelta(days=i)).strftime('%A')
                match_count = data['total']
                total_matches += match_count
                
                status = '✅' if match_count > 0 else '⚪'
                print(f'  {status} {day_name} ({date}): {match_count} matches')
                
                # Show sample matches for days with matches
                if match_count > 0 and i < 3:  # Show samples for first 3 days
                    for j, match in enumerate(data['matches'][:2]):  # Show first 2 matches
                        league = match['league']['name'] if match['league'] else 'No League'
                        print(f'     • {match["home_team"]} vs {match["away_team"]} ({league})')
                        
            else:
                print(f'  ❌ {date}: API error {response.status_code}')
        except Exception as e:
            print(f'  ❌ {date}: Error - {e}')
    
    print(f'\n📊 Total matches across 7 days: {total_matches}')
    print('🎉 Calendar synchronization test completed!')

if __name__ == "__main__":
    test_week_calendar()