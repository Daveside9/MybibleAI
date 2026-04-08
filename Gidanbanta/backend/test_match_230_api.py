#!/usr/bin/env python3
"""
Test Match 230 API - Test if the Arsenal vs Wolves match API is working
"""

import requests
import json

def test_match_230_api():
    """Test accessing match ID 230 through the API"""
    
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
        
        # Test accessing match ID 230 (Arsenal vs Wolves)
        print(f'\n🎯 Testing Arsenal vs Wolves match (ID: 230)...')
        response = requests.get(f"{base_url}/matches/230", headers=headers)
        
        print(f'   Status Code: {response.status_code}')
        print(f'   Response Headers: {dict(response.headers)}')
        
        if response.status_code == 200:
            match_data = response.json()
            print(f'✅ Match found successfully!')
            print(f'   Match: {match_data["home_team"]} vs {match_data["away_team"]}')
            print(f'   Status: {match_data["status"]}')
            print(f'   External ID: {match_data["external_id"]}')
            print(f'   Stream URL: {match_data.get("stream_url", "None")}')
            
            print(f'\n🎉 The match API is working correctly!')
            print(f'   Frontend should be able to load this match')
            
        elif response.status_code == 404:
            print(f'❌ Match not found (404)')
            print(f'   Response: {response.text}')
            print(f'   This means the match is not being returned by the API')
            
        else:
            print(f'❌ Unexpected error: {response.status_code}')
            print(f'   Response: {response.text}')
        
        # Also test if the match appears in today's calendar
        print(f'\n📅 Testing if match appears in today\'s calendar...')
        from datetime import datetime
        today = datetime.now().strftime('%Y-%m-%d')
        
        response = requests.get(
            f"{base_url}/matches/calendar/matches",
            params={"start_date": today, "end_date": today},
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            matches = data.get('matches', [])
            
            # Look for match ID 230
            arsenal_match = None
            for match in matches:
                if match['id'] == 230:
                    arsenal_match = match
                    break
            
            if arsenal_match:
                print(f'✅ Match found in today\'s calendar!')
                print(f'   Status: {arsenal_match["status"]}')
                print(f'   Teams: {arsenal_match["home_team"]} vs {arsenal_match["away_team"]}')
            else:
                print(f'❌ Match NOT found in today\'s calendar')
                print(f'   Total matches today: {len(matches)}')
                print(f'   This might be why the frontend can\'t access it')
        
    except Exception as e:
        print(f'❌ Error during API test: {e}')

if __name__ == "__main__":
    test_match_230_api()