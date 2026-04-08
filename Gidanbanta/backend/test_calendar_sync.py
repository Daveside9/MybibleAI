#!/usr/bin/env python3
"""
Test Calendar Sync Results
"""
import requests
from datetime import datetime, timedelta

def test_calendar_api():
    """Test the calendar API with synchronized data"""
    
    # Test dates
    today = datetime.now().strftime('%Y-%m-%d')
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    
    print('🧪 Testing calendar API with synchronized data...')
    
    # Test today matches
    try:
        response = requests.get(
            f'http://localhost:4000/v1/matches/calendar/matches?start_date={today}&end_date={today}', 
            headers={'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0IiwiZXhwIjoxNzY1NTQxNzU1LCJ0eXBlIjoiYWNjZXNzIn0.1Ve4VRlenOoThwEAJmW3Ls1lfJmpQ-jdyV0tRk7hmt0'}
        )
        if response.status_code == 200:
            data = response.json()
            print(f'✅ Today ({today}): {data["total"]} matches found')
            if data['matches']:
                sample = data['matches'][0]
                league_name = sample['league']['name'] if sample['league'] else 'No league'
                print(f'   Sample: {sample["home_team"]} vs {sample["away_team"]} ({league_name})')
        else:
            print(f'❌ Today API error: {response.status_code}')
    except Exception as e:
        print(f'❌ Today API error: {e}')
    
    # Test tomorrow matches  
    try:
        response = requests.get(
            f'http://localhost:4000/v1/matches/calendar/matches?start_date={tomorrow}&end_date={tomorrow}',
            headers={'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0IiwiZXhwIjoxNzY1NTQxNzU1LCJ0eXBlIjoiYWNjZXNzIn0.1Ve4VRlenOoThwEAJmW3Ls1lfJmpQ-jdyV0tRk7hmt0'}
        )
        if response.status_code == 200:
            data = response.json()
            print(f'✅ Tomorrow ({tomorrow}): {data["total"]} matches found')
            if data['matches']:
                sample = data['matches'][0]
                league_name = sample['league']['name'] if sample['league'] else 'No league'
                print(f'   Sample: {sample["home_team"]} vs {sample["away_team"]} ({league_name})')
        else:
            print(f'❌ Tomorrow API error: {response.status_code}')
    except Exception as e:
        print(f'❌ Tomorrow API error: {e}')
    
    # Test leagues
    try:
        response = requests.get(
            f'http://localhost:4000/v1/matches/calendar/leagues?start_date={today}&end_date={tomorrow}',
            headers={'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0IiwiZXhwIjoxNzY1NTQxNzU1LCJ0eXBlIjoiYWNjZXNzIn0.1Ve4VRlenOoThwEAJmW3Ls1lfJmpQ-jdyV0tRk7hmt0'}
        )
        if response.status_code == 200:
            leagues = response.json()
            print(f'✅ Available leagues: {len(leagues)}')
            for league in leagues[:5]:
                print(f'   {league["name"]}: {league["match_count"]} matches')
        else:
            print(f'❌ Leagues API error: {response.status_code}')
    except Exception as e:
        print(f'❌ Leagues API error: {e}')
    
    # Test league filtering
    if 'leagues' in locals() and leagues:
        test_league = leagues[0]
        try:
            response = requests.get(
                f'http://localhost:4000/v1/matches/calendar/matches?start_date={today}&end_date={tomorrow}&league_id={test_league["id"]}',
                headers={'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0IiwiZXhwIjoxNzY1NTQxNzU1LCJ0eXBlIjoiYWNjZXNzIn0.1Ve4VRlenOoThwEAJmW3Ls1lfJmpQ-jdyV0tRk7hmt0'}
            )
            if response.status_code == 200:
                data = response.json()
                print(f'✅ League filtering ({test_league["name"]}): {data["total"]} matches')
            else:
                print(f'❌ League filtering error: {response.status_code}')
        except Exception as e:
            print(f'❌ League filtering error: {e}')

if __name__ == "__main__":
    test_calendar_api()