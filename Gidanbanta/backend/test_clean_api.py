#!/usr/bin/env python3
"""
Test Clean API - Verify API endpoints return only real matches
"""

import requests
import json
from datetime import datetime, timedelta

def test_clean_api():
    """Test that API endpoints return only real matches"""
    
    base_url = "http://localhost:4000/api/v1"
    
    # Test data
    test_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzY2NzM0NDAwfQ.D6dw4dqZUdFhBjh_bQVQX_HJmhWJc_pNx_aOtherChars"
    headers = {"Authorization": f"Bearer {test_token}"}
    
    try:
        print('🧪 Testing clean API endpoints...')
        
        # Test 1: Today's matches
        print('\n1️⃣ Testing today\'s matches...')
        response = requests.get(f"{base_url}/matches/today", headers=headers)
        if response.status_code == 200:
            matches = response.json()
            print(f'   Found {len(matches)} today matches')
            for i, match in enumerate(matches[:3], 1):
                external_id = match.get('external_id', 'None')
                print(f'   {i}. {match["home_team"]} vs {match["away_team"]} | External ID: {external_id}')
        else:
            print(f'   ❌ Error: {response.status_code}')
        
        # Test 2: Calendar matches for today
        today = datetime.now().strftime('%Y-%m-%d')
        print(f'\n2️⃣ Testing calendar matches for {today}...')
        response = requests.get(
            f"{base_url}/matches/calendar/matches",
            params={"start_date": today, "end_date": today},
            headers=headers
        )
        if response.status_code == 200:
            data = response.json()
            matches = data.get('matches', [])
            print(f'   Found {len(matches)} calendar matches for today')
            print(f'   Total in response: {data.get("total", 0)}')
            
            # Check for mock matches
            mock_count = 0
            for match in matches:
                external_id = match.get('external_id')
                if not external_id or external_id == 0 or (999000 <= external_id <= 999999):
                    mock_count += 1
                    print(f'   ⚠️  Potential mock match: {match["home_team"]} vs {match["away_team"]} | External ID: {external_id}')
            
            if mock_count == 0:
                print(f'   ✅ All matches have valid external IDs')
            else:
                print(f'   ❌ Found {mock_count} potential mock matches')
        else:
            print(f'   ❌ Error: {response.status_code}')
        
        # Test 3: Calendar matches for tomorrow
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        print(f'\n3️⃣ Testing calendar matches for {tomorrow}...')
        response = requests.get(
            f"{base_url}/matches/calendar/matches",
            params={"start_date": tomorrow, "end_date": tomorrow},
            headers=headers
        )
        if response.status_code == 200:
            data = response.json()
            matches = data.get('matches', [])
            print(f'   Found {len(matches)} calendar matches for tomorrow')
            
            # Check for matches with scores (should not exist for future dates)
            scored_matches = 0
            for match in matches:
                if match.get('home_score') is not None or match.get('away_score') is not None:
                    scored_matches += 1
                    print(f'   ⚠️  Future match with score: {match["home_team"]} vs {match["away_team"]} | Score: {match.get("home_score", 0)}-{match.get("away_score", 0)}')
            
            if scored_matches == 0:
                print(f'   ✅ No future matches have scores (correct)')
            else:
                print(f'   ❌ Found {scored_matches} future matches with scores')
        else:
            print(f'   ❌ Error: {response.status_code}')
        
        # Test 4: Available leagues
        print(f'\n4️⃣ Testing available leagues...')
        response = requests.get(
            f"{base_url}/matches/calendar/leagues",
            params={"start_date": today, "end_date": tomorrow},
            headers=headers
        )
        if response.status_code == 200:
            leagues = response.json()
            print(f'   Found {len(leagues)} leagues with matches')
            for i, league in enumerate(leagues[:5], 1):
                print(f'   {i}. {league["name"]} ({league["country"]}) - {league["match_count"]} matches')
            if len(leagues) > 5:
                print(f'   ... and {len(leagues) - 5} more leagues')
        else:
            print(f'   ❌ Error: {response.status_code}')
        
        print(f'\n✅ API testing completed!')
        
    except Exception as e:
        print(f'❌ Error during API testing: {e}')

if __name__ == "__main__":
    test_clean_api()