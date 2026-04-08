#!/usr/bin/env python3
"""
Comprehensive Real Match Fetcher
Fetches real live and upcoming matches from multiple free APIs and saves to database
"""
import asyncio
import httpx
import requests
import json
from datetime import datetime, date, timedelta

def save_matches_to_database(matches):
    """Save matches to database via API"""
    
    print(f"💾 Saving {len(matches)} matches to database...")
    
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
            return False
            
        auth_data = auth_response.json()
        access_token = auth_data.get("access_token")
        headers = {"Authorization": f"Bearer {access_token}"}
        print("✅ Authentication successful")
        
        # 2. Save each match (we'll use a simple approach - check if exists, then add)
        saved_count = 0
        
        for match in matches:
            try:
                # Create match data in the format expected by your backend
                match_data = {
                    "external_id": match.get("id", 0),
                    "title": f"{match['home_team']} vs {match['away_team']}",
                    "home_team": match["home_team"],
                    "away_team": match["away_team"],
                    "home_score": match.get("home_score", 0),
                    "away_score": match.get("away_score", 0),
                    "status": match["status"].lower(),
                    "scheduled_at": match["scheduled_at"],
                    "is_featured": True,  # Mark as featured so it shows in dashboard
                    "stream_url": "https://demo.unified-streaming.com/k8s/features/stable/video/tears-of-steel/tears-of-steel.ism/.m3u8",
                    "home_odds": match.get("home_odds", 2.1),
                    "away_odds": match.get("away_odds", 3.4),
                    "draw_odds": match.get("draw_odds", 3.2)
                }
                
                # For now, we'll print what we would save (since we need database access)
                print(f"   📝 Would save: {match_data['title']} - {match_data['status']}")
                saved_count += 1
                
            except Exception as e:
                print(f"   ❌ Error processing match {match.get('home_team', 'Unknown')} vs {match.get('away_team', 'Unknown')}: {e}")
        
        print(f"✅ Processed {saved_count} matches")
        return True
        
    except Exception as e:
        print(f"❌ Database save failed: {e}")
        return False

async def fetch_football_data_org():
    """Fetch from Football-Data.org API (requires free API key)"""
    
    # Check if API key is available (you can get one free from https://www.football-data.org/client/register)
    api_key = "YOUR_API_KEY_HERE"  # Replace with actual key
    
    if api_key == "YOUR_API_KEY_HERE":
        print("⚠️  Football-Data.org API key not configured")
        return []
    
    print("⚽ Fetching from Football-Data.org...")
    
    matches = []
    
    async with httpx.AsyncClient() as client:
        try:
            # Get today's and tomorrow's matches
            today = date.today()
            tomorrow = today + timedelta(days=1)
            
            response = await client.get(
                "https://api.football-data.org/v4/matches",
                headers={"X-Auth-Token": api_key},
                params={
                    "dateFrom": today.isoformat(),
                    "dateTo": tomorrow.isoformat()
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                api_matches = data.get("matches", [])
                
                for match in api_matches:
                    home_team = match.get("homeTeam", {}).get("name", "Unknown")
                    away_team = match.get("awayTeam", {}).get("name", "Unknown")
                    
                    # Map status
                    status_map = {
                        "LIVE": "live",
                        "IN_PLAY": "live", 
                        "PAUSED": "live",
                        "FINISHED": "finished",
                        "SCHEDULED": "scheduled",
                        "TIMED": "scheduled"
                    }
                    
                    api_status = match.get("status", "SCHEDULED")
                    our_status = status_map.get(api_status, "scheduled")
                    
                    match_info = {
                        "id": match.get("id"),
                        "home_team": home_team,
                        "away_team": away_team,
                        "home_score": match.get("score", {}).get("fullTime", {}).get("home") or 0,
                        "away_score": match.get("score", {}).get("fullTime", {}).get("away") or 0,
                        "status": our_status,
                        "scheduled_at": match.get("utcDate", ""),
                        "league": match.get("competition", {}).get("name", "Unknown League"),
                        "source": "Football-Data.org"
                    }
                    
                    matches.append(match_info)
                
                print(f"   Found {len(matches)} matches from Football-Data.org")
            else:
                print(f"   ❌ API Error: {response.status_code}")
        
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return matches

async def fetch_espn_soccer():
    """Fetch from ESPN Soccer API (free, no key required)"""
    
    print("📺 Fetching from ESPN Soccer API...")
    
    leagues = [
        ("eng.1", "Premier League"),
        ("esp.1", "La Liga"), 
        ("ger.1", "Bundesliga"),
        ("ita.1", "Serie A"),
        ("fra.1", "Ligue 1"),
        ("uefa.champions", "Champions League"),
        ("uefa.europa", "Europa League"),
        ("conmebol.libertadores", "Copa Libertadores"),
        ("concacaf.champions", "CONCACAF Champions League")
    ]
    
    all_matches = []
    
    async with httpx.AsyncClient() as client:
        for league_id, league_name in leagues:
            try:
                print(f"   Checking {league_name}...")
                response = await client.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{league_id}/scoreboard")
                
                if response.status_code == 200:
                    data = response.json()
                    events = data.get("events", [])
                    
                    for event in events:
                        # Get match status
                        status = event.get("status", {}).get("type", {}).get("name", "")
                        
                        # Check if match is today or tomorrow
                        event_date = event.get("date", "")
                        is_relevant = False
                        scheduled_at = ""
                        
                        if event_date:
                            try:
                                match_datetime = datetime.fromisoformat(event_date.replace("Z", "+00:00"))
                                match_date = match_datetime.date()
                                today = date.today()
                                tomorrow = today + timedelta(days=1)
                                
                                if match_date in [today, tomorrow]:
                                    is_relevant = True
                                    scheduled_at = match_datetime.isoformat()
                            except:
                                pass
                        
                        # Include live matches regardless of date
                        if "IN_PROGRESS" in status or "HALFTIME" in status:
                            is_relevant = True
                            if not scheduled_at:
                                scheduled_at = datetime.now().isoformat()
                        
                        if is_relevant:
                            # Get team names and scores
                            competitions = event.get("competitions", [{}])
                            if competitions:
                                competitors = competitions[0].get("competitors", [])
                                if len(competitors) >= 2:
                                    home_team = competitors[0].get("team", {}).get("displayName", "")
                                    away_team = competitors[1].get("team", {}).get("displayName", "")
                                    home_score = int(competitors[0].get("score", 0))
                                    away_score = int(competitors[1].get("score", 0))
                                    
                                    # Map status
                                    our_status = "live" if ("IN_PROGRESS" in status or "HALFTIME" in status) else "scheduled"
                                    if "FINAL" in status:
                                        our_status = "finished"
                                    
                                    match_info = {
                                        "id": int(event.get("id", 0)),
                                        "home_team": home_team,
                                        "away_team": away_team,
                                        "home_score": home_score,
                                        "away_score": away_score,
                                        "status": our_status,
                                        "scheduled_at": scheduled_at,
                                        "league": league_name,
                                        "source": "ESPN"
                                    }
                                    
                                    all_matches.append(match_info)
            
            except Exception as e:
                print(f"   ❌ Error fetching {league_name}: {e}")
    
    print(f"   Found {len(all_matches)} matches from ESPN")
    return all_matches

async def fetch_thesportsdb():
    """Fetch from TheSportsDB API (free, no key required)"""
    
    print("🏆 Fetching from TheSportsDB...")
    
    # Major league IDs
    leagues = [
        (4328, "Premier League"),
        (4335, "La Liga"),
        (4331, "Serie A"),
        (4332, "Bundesliga"),
        (4334, "Ligue 1"),
        (4480, "Champions League")
    ]
    
    all_matches = []
    
    async with httpx.AsyncClient() as client:
        for league_id, league_name in leagues:
            try:
                print(f"   Checking {league_name}...")
                
                # Get live scores
                response = await client.get(f"https://www.thesportsdb.com/api/v1/json/3/livescore.php?l={league_id}")
                
                if response.status_code == 200:
                    data = response.json()
                    events = data.get("events", [])
                    
                    if events:
                        for event in events:
                            home_team = event.get("strHomeTeam", "")
        all_matches.extend(football_data_matches)
        
        thesportsdb_matches = await self.fetch_thesportsdb_matches()
        all_matches.extend(thesportsdb_matches)
        
        # Remove duplicates based on team names
        unique_matches = []
        seen_matches = set()
        
        for match in all_matches:
            match_key = f"{match['home_team'].lower()}_{match['away_team'].lower()}"
            if match_key not in seen_matches:
                unique_matches.append(match)
                seen_matches.add(match_key)
        
        # Categorize matches
        live_matches = [m for m in unique_matches if m['status'] == 'live']
        upcoming_matches = [m for m in unique_matches if m['status'] == 'scheduled']
        finished_matches = [m for m in unique_matches if m['status'] == 'finished']
        
        # Display results
        print(f"\n📊 Match Summary:")
        print(f"   • Total unique matches: {len(unique_matches)}")
        print(f"   • Live matches: {len(live_matches)}")
        print(f"   • Upcoming matches: {len(upcoming_matches)}")
        print(f"   • Finished matches: {len(finished_matches)}")
        
        if live_matches:
            print(f"\n🔴 Live Matches:")
            for match in live_matches:
                print(f"   • {match['title']} ({match['league_name']}) - {match['