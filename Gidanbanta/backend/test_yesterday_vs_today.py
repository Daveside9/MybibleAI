#!/usr/bin/env python3
"""
Test Yesterday vs Today - Compare filtering behavior
"""

import requests
import json
from datetime import datetime, timedelta

def test_yesterday_vs_today():
    """Test filtering differences between yesterday and today"""
    
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
        
        # Test yesterday's matches (should include finished matches)
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        print(f'\n📅 Testing yesterday\'s matches ({yesterday}) - should include finished matches...')
        
        response = requests.get(
            f"{base_url}/matches/calendar/matches",
            params={"start_date": yesterday, "end_date": yesterday},
            headers=headers
        )
        
        yesterday_finished = 0
        yesterday_total = 0
        
        if response.status_code == 200:
            data = response.json()
            matches = data.get('matches', [])
            yesterday_total = len(matches)
            
            for match in matches:
                if match.get('status') == 'finished':
                    yesterday_finished += 1
            
            print(f'   Total matches: {yesterday_total}')
            print(f'   Finished matches: {yesterday_finished}')
        
        # Test today's matches (should exclude finished matches)
        today = datetime.now().strftime('%Y-%m-%d')
        print(f'\n📅 Testing today\'s matches ({today}) - should exclude finished matches...')
        
        response = requests.get(
            f"{base_url}/matches/calendar/matches",
            params={"start_date": today, "end_date": today},
            headers=headers
        )
        
        today_finished = 0
        today_total = 0
        
        if response.status_code == 200:
            data = response.json()
            matches = data.get('matches', [])
            today_total = len(matches)
            
            status_counts = {}
            for match in matches:
                status = match.get('status', 'unknown')
                status_counts[status] = status_counts.get(status, 0) + 1
                if status == 'finished':
                    today_finished += 1
            
            print(f'   Total matches: {today_total}')
            print(f'   Finished matches: {today_finished}')
            print(f'   Status breakdown: {status_counts}')
        
        # Summary
        print(f'\n📊 Filtering Summary:')
        print(f'   Yesterday ({yesterday}): {yesterday_total} matches, {yesterday_finished} finished (all statuses shown)')
        print(f'   Today ({today}): {today_total} matches, {today_finished} finished (finished matches filtered out)')
        
        if today_finished == 0:
            print(f'   ✅ Perfect! Today\'s filtering is working correctly')
        else:
            print(f'   ❌ Issue: Today still shows {today_finished} finished matches')
        
        print(f'\n✅ Comparison test completed!')
        
    except Exception as e:
        print(f'❌ Error during comparison test: {e}')

if __name__ == "__main__":
    test_yesterday_vs_today()