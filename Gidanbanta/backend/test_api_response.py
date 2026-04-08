#!/usr/bin/env python3
"""
Test API Response - Check what the calendar matches endpoint returns
"""
import requests
import json
from datetime import date

def test_api():
    """Test the calendar matches API endpoint"""
    
    print("🔍 Testing Calendar Matches API")
    print("=" * 50)
    
    base_url = "http://localhost:4000"
    today = date.today().isoformat()
    
    # Test without authentication first
    url = f"{base_url}/v1/matches/calendar/matches?start_date={today}&end_date={today}"
    
    try:
        print(f"📡 Calling: {url}")
        response = requests.get(url)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            matches = data.get("matches", [])
            
            print(f"✅ Success! Found {len(matches)} matches")
            print(f"📈 Total: {data.get('total', 0)}")
            print(f"💾 Cached: {data.get('cached', False)}")
            
            print(f"\n🎯 First 5 Matches:")
            for i, match in enumerate(matches[:5]):
                status_icon = "🔴" if match.get("status") == "LIVE" else "⏰"
                print(f"   {i+1}. {status_icon} {match.get('home_team')} vs {match.get('away_team')}")
                print(f"      Status: {match.get('status')}")
                print(f"      Time: {match.get('scheduled_time', 'N/A')}")
                print(f"      League: {match.get('league', {}).get('name', 'Unknown')}")
                print()
            
            # Check for specific real matches
            real_matches = [m for m in matches if "Celtic" in m.get("home_team", "") or "Celtic" in m.get("away_team", "")]
            real_matches += [m for m in matches if "Basel" in m.get("home_team", "") or "Basel" in m.get("away_team", "")]
            real_matches += [m for m in matches if "Dinamo Zagreb" in m.get("home_team", "") or "Dinamo Zagreb" in m.get("away_team", "")]
            
            if real_matches:
                print(f"⚽ Found Real Matches:")
                for match in real_matches:
                    print(f"   • {match.get('home_team')} vs {match.get('away_team')} - {match.get('status')}")
            else:
                print(f"❌ No real matches found in API response")
                print(f"   The API is still returning old mock matches")
        
        elif response.status_code == 401:
            print(f"🔐 Authentication required. Let's try with a test user...")
            
            # Try to login first
            login_url = f"{base_url}/v1/auth/login"
            login_data = {
                "email": "test@example.com",
                "password": "testpassword"
            }
            
            login_response = requests.post(login_url, json=login_data)
            
            if login_response.status_code == 200:
                token = login_response.json().get("access_token")
                headers = {"Authorization": f"Bearer {token}"}
                
                print(f"✅ Login successful, retrying with token...")
                
                # Retry with authentication
                response = requests.get(url, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    matches = data.get("matches", [])
                    
                    print(f"✅ Success! Found {len(matches)} matches")
                    
                    print(f"\n🎯 First 5 Matches:")
                    for i, match in enumerate(matches[:5]):
                        status_icon = "🔴" if match.get("status") == "LIVE" else "⏰"
                        print(f"   {i+1}. {status_icon} {match.get('home_team')} vs {match.get('away_team')}")
                        print(f"      Status: {match.get('status')}")
                        print(f"      League: {match.get('league', {}).get('name', 'Unknown')}")
                else:
                    print(f"❌ Still failed: {response.status_code}")
                    print(f"Response: {response.text}")
            else:
                print(f"❌ Login failed: {login_response.status_code}")
                print(f"Response: {login_response.text}")
        
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
    
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_api()