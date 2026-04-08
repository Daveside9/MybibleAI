#!/usr/bin/env python3
"""
Test Tomorrow Clean - Verify tomorrow's matches have no scores
"""

import requests
import json
from datetime import datetime, timedelta

def test_tomorrow_clean():
    """Test that tomorrow's matches have no scores"""
    
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
        
        # Test calendar matches for tomorrow
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        print(f'\n📅 Testing tomorrow\'s matches ({tomorrow})...')
        
        response = requests.get(
            f"{base_url}/matches/calendar/matches",
            params={"start_date": tomorrow, "end_date": tomorrow},
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            matches = data.get('matches', [])
            print(f'✅ Found {len(matches)} matches for tomorrow')
            
            # Check for matches with scores (should be ZERO)
            matches_with_scores = 0
            for match in matches:
                home_score = match.get('home_score')
                away_score = match.get('away_score')
                if home_score is not None or away_score is not None:
                    matches_with_scores += 1
                    print(f'❌ Future match with score: {match["home_team"]} vs {match["away_team"]} | Score: {home_score}-{away_score}')
            
            if matches_with_scores == 0:
                print(f'🎉 Perfect! No future matches have scores')
                
                # Show sample matches
                for i, match in enumerate(matches[:3], 1):
                    league = match.get('league', {}).get('name', 'No League') if match.get('league') else 'No League'
                    print(f'   {i}. {match["home_team"]} vs {match["away_team"]} | League: {league} | No Score ✅')
            else:
                print(f'❌ Found {matches_with_scores} future matches with scores!')
                
        else:
            print(f'❌ Tomorrow matches failed: {response.status_code} - {response.text}')
        
        print(f'\n✅ Tomorrow test completed!')
        
    except Exception as e:
        print(f'❌ Error during tomorrow test: {e}')

if __name__ == "__main__":
    test_tomorrow_clean()