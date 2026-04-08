#!/usr/bin/env python3
"""
Test League Filtering - Check if league filtering works correctly
"""
import requests
import json
from datetime import date

def test_league_filtering():
    """Test the league filtering API"""
    
    print("🔍 Testing League Filtering")
    print("=" * 50)
    
    base_url = "http://localhost:4000"
    today = date.today().isoformat()
    
    try:
        # 1. Login first
        print("🔐 Logging in...")
        auth_response = requests.post(f"{base_url}/v1/auth/login", json={
            "email": "test@example.com",
            "password": "testpassword"
        })
        
        if auth_response.status_code != 200:
            print(f"❌ Login failed: {auth_response.status_code}")
            return
            
        token = auth_response.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        print("✅ Login successful")
        
        # 2. Get available leagues
        print(f"\n📋 Getting available leagues...")
        leagues_url = f"{base_url}/v1/matches/calendar/leagues?start_date={today}&end_date={today}"
        leagues_response = requests.get(leagues_url, headers=headers)
        
        if leagues_response.status_code == 200:
            leagues = leagues_response.json()
            print(f"✅ Found {len(leagues)} leagues:")
            for league in leagues[:5]:  # Show first 5
                print(f"   🏆 {league['name']} (ID: {league['id']}) - {league['match_count']} matches")
        else:
            print(f"❌ Failed to get leagues: {leagues_response.status_code}")
            return
        
        # 3. Test filtering by specific league (UEFA Europa League should be ID 5)
        europa_league_id = None
        for league in leagues:
            if "Europa League" in league['name']:
                europa_league_id = league['id']
                break
        
        if europa_league_id:
            print(f"\n🔍 Testing Europa League filtering (ID: {europa_league_id})...")
            matches_url = f"{base_url}/v1/matches/calendar/matches?start_date={today}&end_date={today}&league_id={europa_league_id}"
            matches_response = requests.get(matches_url, headers=headers)
            
            if matches_response.status_code == 200:
                data = matches_response.json()
                matches = data.get("matches", [])
                print(f"✅ Europa League matches: {len(matches)}")
                
                # Check if all matches are actually Europa League
                europa_matches = 0
                other_matches = 0
                
                for match in matches[:10]:  # Check first 10
                    league_name = match.get('league', {}).get('name', 'Unknown') if match.get('league') else 'No League'
                    if "Europa League" in league_name:
                        europa_matches += 1
                    else:
                        other_matches += 1
                        print(f"   ❌ Non-Europa match: {match.get('home_team')} vs {match.get('away_team')} - {league_name}")
                
                print(f"   ✅ Europa League matches: {europa_matches}")
                print(f"   ❌ Other league matches: {other_matches}")
                
                if other_matches == 0:
                    print(f"   🎉 League filtering is working correctly!")
                else:
                    print(f"   ⚠️  League filtering has issues - showing matches from other leagues")
            else:
                print(f"❌ Failed to get Europa League matches: {matches_response.status_code}")
        
        # 4. Test all matches (no league filter)
        print(f"\n🔍 Testing all matches (no filter)...")
        all_matches_url = f"{base_url}/v1/matches/calendar/matches?start_date={today}&end_date={today}"
        all_matches_response = requests.get(all_matches_url, headers=headers)
        
        if all_matches_response.status_code == 200:
            data = all_matches_response.json()
            all_matches = data.get("matches", [])
            print(f"✅ All matches: {len(all_matches)}")
            
            # Count by league
            league_counts = {}
            for match in all_matches:
                league_name = match.get('league', {}).get('name', 'Unknown') if match.get('league') else 'No League'
                league_counts[league_name] = league_counts.get(league_name, 0) + 1
            
            print(f"   📊 Matches by league:")
            for league_name, count in sorted(league_counts.items(), key=lambda x: x[1], reverse=True):
                print(f"      🏆 {league_name}: {count} matches")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_league_filtering()