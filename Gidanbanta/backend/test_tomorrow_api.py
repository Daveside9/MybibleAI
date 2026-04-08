#!/usr/bin/env python3
"""
Test the calendar API for tomorrow's matches to see what's returned
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import requests
from datetime import datetime, timedelta
import json

def test_tomorrow_api():
    """Test the calendar API for tomorrow's matches"""
    
    # Calculate tomorrow's date
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow_str = tomorrow.strftime('%Y-%m-%d')
    
    print(f'Testing API for tomorrow: {tomorrow_str}')
    print('=' * 50)
    
    # API endpoint
    base_url = "http://localhost:4000"
    endpoint = f"{base_url}/api/v1/matches/calendar/matches"
    
    # Test parameters
    params = {
        'start_date': tomorrow_str,
        'end_date': tomorrow_str
    }
    
    # You'll need to get a valid token - for now let's try without auth first
    headers = {
        'Content-Type': 'application/json'
    }
    
    try:
        print(f"Making request to: {endpoint}")
        print(f"Parameters: {params}")
        
        response = requests.get(endpoint, params=params, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            matches = data.get('matches', [])
            
            print(f"Total matches returned: {len(matches)}")
            print()
            
            for i, match in enumerate(matches, 1):
                print(f"Match {i}: {match.get('home_team')} vs {match.get('away_team')}")
                print(f"  External ID: {match.get('external_id')}")
                print(f"  League: {match.get('league', {}).get('name', 'Unknown')}")
                print(f"  Scheduled: {match.get('scheduled_time')}")
                print()
                
        elif response.status_code == 401:
            print("Authentication required. Need to provide valid token.")
            print("Response:", response.text)
        else:
            print(f"Error response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("Could not connect to the API. Make sure the backend is running on port 4000.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_tomorrow_api()