#!/usr/bin/env python3
"""
Test Sporting with Auth - Test the Sporting CP match API with proper authentication
"""

import requests
import json

def test_sporting_with_auth():
    """Test the match API with authentication"""
    
    try:
        print('🔍 Testing Sporting CP match API with authentication...')
        
        # First, login to get a token
        print('🔐 Logging in to get authentication token...')
        
        login_data = {
            "email": "admin@matchhang.com",
            "password": "Admin@123"
        }
        
        login_response = requests.post(
            'http://localhost:4000/v1/auth/login',
            json=login_data
        )
        
        if login_response.status_code != 200:
            print(f'❌ Login failed: {login_response.status_code}')
            print(f'Response: {login_response.text}')
            return
        
        login_result = login_response.json()
        token = login_result.get('access_token')
        
        if not token:
            print('❌ No access token received from login')
            return
        
        print('✅ Login successful, got access token')
        
        # Now test the match endpoint with authentication
        print('🔍 Testing match endpoint with authentication...')
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        match_response = requests.get(
            'http://localhost:4000/v1/matches/417',
            headers=headers
        )
        
        print(f'Status Code: {match_response.status_code}')
        
        if match_response.status_code == 200:
            data = match_response.json()
            print(f'✅ API Response:')
            print(f'   Match: {data.get("home_team")} vs {data.get("away_team")}')
            print(f'   Status: {data.get("status")}')
            print(f'   Stream URL: {data.get("stream_url")}')
            print(f'   External ID: {data.get("external_id")}')
            
            if data.get("stream_url"):
                print(f'✅ Stream URL is present in API response!')
                print(f'   URL: {data.get("stream_url")}')
                print(f'\n🎉 SUCCESS! The live stream is working!')
                print(f'   Visit: http://localhost:3000/match/417')
                print(f'   You should see the video player with the test stream')
            else:
                print(f'❌ Stream URL is missing from API response!')
                
        else:
            print(f'❌ API Error: {match_response.status_code}')
            print(f'Response: {match_response.text}')
            
    except requests.exceptions.ConnectionError:
        print('❌ Cannot connect to backend server!')
        print('   Make sure the backend is running on http://localhost:4000')
    except Exception as e:
        print(f'❌ Error testing API: {e}')

if __name__ == "__main__":
    test_sporting_with_auth()