#!/usr/bin/env python3
"""
Test Deleted Match API - Test accessing a deleted match ID
"""

import requests

def test_deleted_match_api():
    """Test accessing a deleted match ID through the API"""
    
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
        
        # Test accessing deleted match IDs (these should return 404)
        deleted_match_ids = [83, 197, 198, 199, 200]  # From our missing IDs list
        
        print(f'\n🧪 Testing deleted match IDs...')
        for match_id in deleted_match_ids:
            response = requests.get(f"{base_url}/matches/{match_id}", headers=headers)
            
            if response.status_code == 404:
                print(f'   ✅ Match ID {match_id}: 404 Not Found (correct)')
            else:
                print(f'   ❌ Match ID {match_id}: {response.status_code} - {response.text}')
        
        # Test accessing an existing match ID (should work)
        print(f'\n🧪 Testing existing match ID...')
        response = requests.get(f"{base_url}/matches/6", headers=headers)  # ID 6 exists
        
        if response.status_code == 200:
            match_data = response.json()
            print(f'   ✅ Match ID 6: {match_data["home_team"]} vs {match_data["away_team"]} (working)')
        else:
            print(f'   ❌ Match ID 6: {response.status_code} - {response.text}')
        
        print(f'\n✅ API test completed!')
        
    except Exception as e:
        print(f'❌ Error during API test: {e}')

if __name__ == "__main__":
    test_deleted_match_api()