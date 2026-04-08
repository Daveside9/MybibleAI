#!/usr/bin/env python3
"""
Simple API Test - Login and test matches endpoint
"""

import requests
import json
from datetime import datetime

def test_api_simple():
    """Test API with proper authentication"""
    
    base_url = "http://localhost:4000/v1"
    
    try:
        print('🔐 Logging in...')
        
        # Login to get a valid token
        login_data = {
            "email": "test@example.com",
            "password": "testpassword"
        }
        
        response = requests.post(f"{base_url}/auth/login", json=login_data)
        if response.status_code != 200:
            print(f'❌ Login failed: {response.status_code} - {response.text}')
            return
        
        token_data = response.json()
        token = token_data.get('access_token')
        print(f'✅ Login successful')
        
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test calendar matches for today
        today = datetime.now().strftime('%Y-%m-%d')
        print(f'\n📅 Testing calendar matches for {today}...')
        
        response = requests.get(
            f"{base_url}/matches/calendar/matches",
            params={"start_date": today, "end_date": today},
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            matches = data.get('matches', [])
            print(f'✅ Found {len(matches)} matches for today')
            print(f'   Total: {data.get("total", 0)}')
            print(f'   Cached: {data.get("cached", False)}')
            
            # Show sample matches
            for i, match in enumerate(matches[:3], 1):
                external_id = match.get('external_id', 'None')
                league = match.get('league', {}).get('name', 'No League') if match.get('league') else 'No League'
                print(f'   {i}. {match["home_team"]} vs {match["away_team"]} | League: {league} | External ID: {external_id}')
            
            # Check for any mock matches
            mock_count = 0
            for match in matches:
                external_id = match.get('external_id')
                if not external_id or external_id == 0 or (999000 <= external_id <= 999999):
                    mock_count += 1
            
            if mock_count == 0:
                print(f'✅ All matches have valid external IDs - no mock matches found!')
            else:
                print(f'❌ Found {mock_count} potential mock matches')
                
        else:
            print(f'❌ Calendar matches failed: {response.status_code} - {response.text}')
        
        # Test available leagues
        print(f'\n🏆 Testing available leagues...')
        response = requests.get(
            f"{base_url}/matches/calendar/leagues",
            params={"start_date": today, "end_date": today},
            headers=headers
        )
        
        if response.status_code == 200:
            leagues = response.json()
            print(f'✅ Found {len(leagues)} leagues with matches today')
            for i, league in enumerate(leagues[:5], 1):
                print(f'   {i}. {league["name"]} ({league["country"]}) - {league["match_count"]} matches')
        else:
            print(f'❌ Leagues failed: {response.status_code} - {response.text}')
        
        print(f'\n🎉 API test completed successfully!')
        
    except Exception as e:
        print(f'❌ Error during API test: {e}')

if __name__ == "__main__":
    test_api_simple()