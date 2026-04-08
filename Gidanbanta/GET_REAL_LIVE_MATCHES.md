# 🔴 Get Real Live Matches - Complete Guide

## 🎯 Quick Start (No API Key Required)

Your streaming functionality is already working! You have **6 live matches** in your database. Here's how to get REAL live match data:

### Option 1: ESPN API (Free, No Registration) ⚡

```bash
# Run this anytime to get real live matches
cd Gidanbanta/backend
python setup_real_live_matches.py
```

**When it works best:**
- During European football hours (12:00-22:00 UTC)
- Weekends (Premier League, La Liga, etc.)
- Weekday evenings (Champions League, etc.)

### Option 2: Football-Data.org (Free with Registration) 🆓

**Step 1: Get Free API Key**
1. Go to: https://www.football-data.org/client/register
2. Fill out the form (takes 30 seconds)
3. Verify your email
4. Copy your API token

**Step 2: Add to Environment**
```bash
# Add to Gidanbanta/backend/.env
FOOTBALL_DATA_TOKEN=your_token_here
```

**Step 3: Run Script**
```bash
cd Gidanbanta/backend
python setup_real_live_matches.py
```

**Benefits:**
- ✅ 100 requests per day (free)
- ✅ More reliable than ESPN
- ✅ Covers major European leagues
- ✅ Real-time live scores

## 🕒 When to Find Live Matches

### Best Times (UTC):
- **Saturday 12:00-18:00** - Premier League, Bundesliga
- **Sunday 13:00-20:00** - La Liga, Serie A
- **Tuesday/Wednesday 19:00-22:00** - Champions League
- **Thursday 17:00-22:00** - Europa League

### Current Status:
```bash
# Check what's live right now
python -c "
import asyncio
import httpx

async def check_live():
    # ESPN check
    async with httpx.AsyncClient() as client:
        response = await client.get('https://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/scoreboard')
        if response.status_code == 200:
            data = response.json()
            live_count = sum(1 for event in data.get('events', []) 
                           if 'IN_PROGRESS' in event.get('status', {}).get('type', {}).get('name', ''))
            print(f'🔴 Live Premier League matches: {live_count}')

asyncio.run(check_live())
"
```

## 🔧 Advanced Setup: Multiple APIs

Create a comprehensive live match fetcher:

```python
# Create: backend/get_all_live_matches.py
import asyncio
import httpx
import os
from datetime import datetime

async def get_all_live_matches():
    \"\"\"Get live matches from multiple free sources\"\"\"
    
    all_matches = []
    
    # 1. ESPN API (Free, no key)
    print("📺 Checking ESPN...")
    leagues = ["eng.1", "esp.1", "ger.1", "ita.1", "fra.1"]
    
    async with httpx.AsyncClient() as client:
        for league in leagues:
            try:
                response = await client.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{league}/scoreboard")
                if response.status_code == 200:
                    data = response.json()
                    for event in data.get("events", []):
                        status = event.get("status", {}).get("type", {}).get("name", "")
                        if "IN_PROGRESS" in status:
                            all_matches.append({
                                "source": "ESPN",
                                "league": league,
                                "name": event.get("name"),
                                "status": status
                            })
            except:
                pass
    
    # 2. Football-Data.org (if token available)
    token = os.getenv("FOOTBALL_DATA_TOKEN")
    if token:
        print("⚽ Checking Football-Data.org...")
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    "https://api.football-data.org/v4/matches",
                    headers={"X-Auth-Token": token},
                    params={"status": "LIVE"}
                )
                if response.status_code == 200:
                    data = response.json()
                    for match in data.get("matches", []):
                        all_matches.append({
                            "source": "Football-Data.org",
                            "league": match.get("competition", {}).get("name"),
                            "name": f"{match.get('homeTeam', {}).get('name')} vs {match.get('awayTeam', {}).get('name')}",
                            "status": match.get("status")
                        })
            except Exception as e:
                print(f"Football-Data.org error: {e}")
    
    # 3. TheSportsDB (Free backup)
    print("🏆 Checking TheSportsDB...")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("https://www.thesportsdb.com/api/v1/json/3/livescore.php?l=4328")  # Premier League
            if response.status_code == 200:
                data = response.json()
                if data.get("events"):
                    for event in data["events"]:
                        all_matches.append({
                            "source": "TheSportsDB",
                            "league": "Premier League",
                            "name": f"{event.get('strHomeTeam')} vs {event.get('strAwayTeam')}",
                            "status": "LIVE"
                        })
        except:
            pass
    
    return all_matches

if __name__ == "__main__":
    matches = asyncio.run(get_all_live_matches())
    
    if matches:
        print(f"\n🔴 Found {len(matches)} live matches:")
        for match in matches:
            print(f"   {match['source']}: {match['name']} ({match['league']})")
    else:
        print("\n⏰ No live matches found right now")
        print("   Try again during match hours!")
```

## 🚀 Production Setup

For a production app, I recommend this approach:

### 1. **Primary API: Football-Data.org**
- Free tier: 100 requests/day
- Reliable and official
- Good for development

### 2. **Backup API: ESPN**
- Unlimited requests
- No registration required
- Good fallback option

### 3. **Scheduled Updates**
```python
# Add to your cron job or task scheduler
# Run every 5 minutes during match hours
*/5 12-22 * * 0,6 python setup_real_live_matches.py
```

## 🎬 Test Your Setup

1. **Check current live matches:**
```bash
cd Gidanbanta/backend
python setup_real_live_matches.py
```

2. **Visit your app:**
```bash
# Frontend should be running on:
http://localhost:3000

# Login with:
Email: test@example.com
Password: testpassword
```

3. **Navigate to a live match:**
```bash
# Go to any match with LIVE status
http://localhost:3000/match/1
```

## 📊 API Comparison

| API | Free Requests | Registration | Live Data | Reliability |
|-----|---------------|--------------|-----------|-------------|
| Football-Data.org | 100/day | Required | ✅ Yes | ⭐⭐⭐⭐⭐ |
| ESPN | Unlimited | None | ✅ Yes | ⭐⭐⭐⭐ |
| TheSportsDB | Unlimited | None | ⚠️ Limited | ⭐⭐⭐ |
| API-Football | 100/day | Required | ✅ Yes | ⭐⭐⭐⭐⭐ |

## 🎯 Next Steps

1. **Get Football-Data.org token** (recommended)
2. **Run the setup script** during match hours
3. **Test with real live matches**
4. **Set up automated updates** for production

Your streaming functionality is ready - you just need real live match data! 🚀