#!/usr/bin/env python3
"""
Test Stream API - Check if the stream URL is being returned correctly
"""

import requests
import json

def test_stream_api():
    """Test the match API to see if stream URL is returned"""
    
    try:
        print('🔍 Testing match API for Arsenal vs Wolves (ID: 230)...')
        
        # Test the API endpoint
        response = requests.get('http://localhost:4000/api/v1/matches/230')
        
        print(f'Status Code: {response.status_code}')
        
        if response.status_code == 200:
            data = response.json()
            print(f'✅ API Response:')
            print(f'   Match: {data.get("home_team")} vs {data.get("away_team")}')
            print(f'   Status: {data.get("status")}')
            print(f'   Stream URL: {data.get("stream_url")}')
            
            if data.get("stream_url"):
                print(f'✅ Stream URL is present in API response!')
                print(f'   URL: {data.get("stream_url")}')
            else:
                print(f'❌ Stream URL is missing from API response!')
                
        else:
            print(f'❌ API Error: {response.status_code}')
            print(f'Response: {response.text}')
            
    except requests.exceptions.ConnectionError:
        print('❌ Cannot connect to backend server!')
        print('   Make sure the backend is running on http://localhost:4000')
        print('   Run: cd backend && .\venv\Scripts\python.exe main.py')
    except Exception as e:
        print(f'❌ Error testing API: {e}')

if __name__ == "__main__":
    test_stream_api()