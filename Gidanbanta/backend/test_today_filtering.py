#!/usr/bin/env python3
"""
Test Today Filtering - Verify today's matches only show live and upcoming
"""

import requests
import json
from datetime import datetime

def test_today_filtering():
    """Test that today's matches only show live and upcoming matches"""
    
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
        
        # Test today's matches
        today = datetime.now().strftime('%Y-%m-%d')
        print(f'\n📅 Testing today\'s matches ({today}) - should only show live and upcoming...')
        
        response = requests.get(
            f"{base_url}/matches/calendar/matches",
            params={"start_date": today, "end_date": today},
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            matches = data.get('matches', [])
            print(f'✅ Found {len(matches)} matches for today')
            
            # Check match statuses
            status_counts = {}
            finished_matches = []
            
            for match in matches:
                status = match.get('status', 'unknown')
                status_counts[status] = status_counts.get(status, 0) + 1
                
                if status == 'finished':
                    finished_matches.append(match)
            
            print(f'\n📊 Match status breakdown:')
            for status, count in status_counts.items():
                print(f'   {status}: {count} matches')
            
            if finished_matches:
                print(f'\n❌ Found {len(finished_matches)} finished matches (should be 0):')
                for match in finished_matches[:3]:
                    score = f"{match.get('home_score', 0)}-{match.get('away_score', 0)}"
                    print(f'   {match["home_team"]} vs {match["away_team"]} | Score: {score} | Status: {match["status"]}')
            else:
                print(f'\n✅ Perfect! No finished matches found for today')
                print(f'   Only showing live and upcoming matches as requested')
            
            # Show sample matches
            print(f'\n📋 Sample today\'s matches:')
            for i, match in enumerate(matches[:5], 1):
                league = match.get('league', {}).get('name', 'No League') if match.get('league') else 'No League'
                status = match.get('status', 'unknown')
                scheduled_time = match.get('scheduled_time', '')
                if scheduled_time:
                    time_part = scheduled_time.split('T')[1][:5] if 'T' in scheduled_time else ''
                    print(f'   {i}. {match["home_team"]} vs {match["away_team"]} | {status.upper()} | {time_part} | {league}')
                else:
                    print(f'   {i}. {match["home_team"]} vs {match["away_team"]} | {status.upper()} | {league}')
                
        else:
            print(f'❌ Today matches failed: {response.status_code} - {response.text}')
        
        print(f'\n✅ Today filtering test completed!')
        
    except Exception as e:
        print(f'❌ Error during today filtering test: {e}')

if __name__ == "__main__":
    test_today_filtering()