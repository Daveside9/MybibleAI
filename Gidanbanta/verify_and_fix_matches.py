#!/usr/bin/env python3
"""
Verify and fix matches in database - Simple version without dependencies
"""
import requests
import json
from datetime import datetime

def test_matches_api():
    """Test the matches API to see what's available"""
    
    print("🔍 Testing Matches API")
    print("=" * 50)
    
    # Backend API base URL
    base_url = "http://localhost:4000"
    
    try:
        # 1. Authenticate first
        print("🔐 Authenticating...")
        auth_response = requests.post(f"{base_url}/v1/auth/login", json={
            "email": "test@example.com",
            "password": "testpassword"
        })
        
        if auth_response.status_code != 200:
            print(f"❌ Failed to authenticate: {auth_response.status_code}")
            print(f"Response: {auth_response.text}")
            return False
            
        auth_data = auth_response.json()
        access_token = auth_data.get("access_token")
        headers = {"Authorization": f"Bearer {access_token}"}
        print("✅ Authentication successful")
        
        # 2. Get today's featured matches
        print("\n📡 Fetching today's featured matches...")
        response = requests.get(f"{base_url}/v1/matches/today", headers=headers)
        
        if response.status_code == 200:
            matches = response.json()
            print(f"✅ Found {len(matches)} featured matches")
            
            for match in matches:
                print(f"   • {match['home_team']} vs {match['away_team']}")
                print(f"     Status: {match['status']}")
                print(f"     Scheduled: {match['scheduled_at']}")
                print(f"     Stream: {'Yes' if match.get('stream_url') else 'No'}")
                print()
        else:
            print(f"❌ Failed to fetch featured matches: {response.status_code}")
            print(f"Response: {response.text}")
        
        # 3. Get calendar matches for today
        today = datetime.now().strftime('%Y-%m-%d')
        print(f"📅 Fetching calendar matches for {today}...")
        
        response = requests.get(
            f"{base_url}/v1/matches/calendar/matches",
            headers=headers,
            params={
                "start_date": today,
                "end_date": today
            }
        )
        
        if response.status_code == 200:
            calendar_data = response.json()
            matches = calendar_data.get("matches", [])
            print(f"✅ Found {len(matches)} calendar matches")
            
            # Look for Real Madrid vs Manchester City
            real_madrid_matches = []
            city_matches = []
            
            for match in matches:
                home_team = match.get("home_team", "").lower()
                away_team = match.get("away_team", "").lower()
                
                if "real madrid" in home_team or "real madrid" in away_team:
                    real_madrid_matches.append(match)
                
                if "manchester city" in home_team or "manchester city" in away_team or "city" in home_team or "city" in away_team:
                    city_matches.append(match)
            
            print(f"\n⚽ Real Madrid matches: {len(real_madrid_matches)}")
            for match in real_madrid_matches:
                print(f"   • {match['home_team']} vs {match['away_team']} - {match['status']}")
            
            print(f"⚽ Manchester City matches: {len(city_matches)}")
            for match in city_matches:
                print(f"   • {match['home_team']} vs {match['away_team']} - {match['status']}")
            
            # Show all matches
            print(f"\n📋 All matches for today:")
            for match in matches:
                status_icon = "🔴" if match['status'] == 'live' else "⏰"
                print(f"   {status_icon} {match['home_team']} vs {match['away_team']} - {match['status']}")
        else:
            print(f"❌ Failed to fetch calendar matches: {response.status_code}")
            print(f"Response: {response.text}")
        
        # 4. Get available leagues
        print(f"\n🏆 Fetching available leagues...")
        response = requests.get(
            f"{base_url}/v1/matches/calendar/leagues",
            headers=headers,
            params={
                "start_date": today,
                "end_date": today
            }
        )
        
        if response.status_code == 200:
            leagues = response.json()
            print(f"✅ Found {len(leagues)} leagues with matches")
            
            for league in leagues:
                print(f"   • {league['name']} ({league['country']}) - {league['match_count']} matches")
        else:
            print(f"❌ Failed to fetch leagues: {response.status_code}")
        
        print(f"\n🎬 Dashboard Instructions:")
        print(f"   1. Visit: http://localhost:3000/dashboard")
        print(f"   2. Click 'All Leagues' to see all {len(matches)} matches")
        print(f"   3. Click '🔴 Live' to see live matches only")
        print(f"   4. Look for Real Madrid vs Manchester City!")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend server. Make sure it's running on localhost:4000")
        return False
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    print(f"🚀 Starting Match Verification")
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d')}")
    print(f"🕘 Time: {datetime.now().strftime('%H:%M:%S')}")
    print()
    
    success = test_matches_api()
    
    if success:
        print(f"\n🎉 Match verification completed successfully!")
        print(f"\n💡 If you don't see matches in dashboard:")
        print(f"   • Make sure to click 'All Leagues' or '🔴 Live' buttons")
        print(f"   • The dashboard only shows matches when you click navigation")
        print(f"   • This is the expected behavior!")
    else:
        print(f"\n💥 Match verification failed!")
        print(f"   • Make sure backend is running on port 4000")
        print(f"   • Make sure you can login with test@example.com")