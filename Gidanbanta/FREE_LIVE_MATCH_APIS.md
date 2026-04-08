# Free Live Match APIs Guide

## 🆓 Best Free Football APIs for Live Matches

### 1. **API-Football (RapidAPI) - RECOMMENDED** ⭐
- **URL:** https://rapidapi.com/api-sports/api/api-football
- **Free Tier:** 100 requests/day
- **Live Matches:** ✅ Yes
- **Features:** Live scores, fixtures, odds, statistics
- **Status:** Already integrated in your project

**Setup:**
```bash
# Get free API key from RapidAPI
# Add to your .env file:
FOOTBALL_API_KEY=your_rapidapi_key_here
RAPIDAPI_HOST=api-football-v1.p.rapidapi.com
```

### 2. **Football-Data.org** 🆓
- **URL:** https://www.football-data.org/
- **Free Tier:** 10 requests/minute, 100/day
- **Live Matches:** ✅ Yes (limited leagues)
- **Features:** Live scores, fixtures, standings

**Setup:**
```python
# Free API - no credit card required
BASE_URL = "https://api.football-data.org/v4"
headers = {"X-Auth-Token": "your_free_token"}
```

### 3. **TheSportsDB** 🆓
- **URL:** https://www.thesportsdb.com/api.php
- **Free Tier:** Unlimited (with rate limits)
- **Live Matches:** ⚠️ Limited live data
- **Features:** Match data, team info, leagues

### 4. **SportRadar (Free Tier)** 🆓
- **URL:** https://developer.sportradar.com/
- **Free Tier:** 1000 requests/month
- **Live Matches:** ✅ Yes
- **Features:** Real-time scores, detailed stats

### 5. **ESPN API (Unofficial)** 🆓
- **URL:** Various endpoints
- **Free Tier:** Unlimited (unofficial)
- **Live Matches:** ✅ Yes
- **Features:** Live scores, schedules

## 🚀 Quick Setup for Real Live Matches

### Option 1: Use Your Existing API-Football Setup

1. **Get RapidAPI Key:**
   - Go to https://rapidapi.com/api-sports/api/api-football
   - Sign up for free account
   - Subscribe to free tier (100 requests/day)
   - Copy your API key

2. **Update Environment:**
```bash
# In Gidanbanta/backend/.env
FOOTBALL_API_KEY=your_rapidapi_key_here
RAPIDAPI_HOST=api-football-v1.p.rapidapi.com
```

3. **Test Live Matches:**
```python
# Run this script to get live matches
python sync_real_matches.py
```

### Option 2: Football-Data.org (Completely Free)

1. **Get Free Token:**
   - Go to https://www.football-data.org/client/register
   - Register for free (no credit card)
   - Get your free API token

2. **Create New Service:**
```python
# Create: backend/app/services/football_data_free.py
import httpx
from typing import List, Dict

class FootballDataAPI:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://api.football-data.org/v4"
        self.headers = {"X-Auth-Token": token}
    
    async def get_live_matches(self) -> List[Dict]:
        """Get currently live matches"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/matches",
                headers=self.headers,
                params={"status": "LIVE"}
            )
            if response.status_code == 200:
                data = response.json()
                return data.get("matches", [])
        return []
    
    async def get_todays_matches(self) -> List[Dict]:
        """Get today's matches"""
        from datetime import date
        today = date.today().isoformat()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/matches",
                headers=self.headers,
                params={"dateFrom": today, "dateTo": today}
            )
            if response.status_code == 200:
                data = response.json()
                return data.get("matches", [])
        return []
```

### Option 3: ESPN API (Unofficial but Free)

```python
# Create: backend/app/services/espn_api.py
import httpx
from typing import List, Dict

class ESPNSoccerAPI:
    def __init__(self):
        self.base_url = "https://site.api.espn.com/apis/site/v2/sports/soccer"
    
    async def get_live_matches(self) -> List[Dict]:
        """Get live soccer matches from ESPN"""
        async with httpx.AsyncClient() as client:
            # Premier League
            response = await client.get(f"{self.base_url}/eng.1/scoreboard")
            if response.status_code == 200:
                data = response.json()
                live_matches = []
                for event in data.get("events", []):
                    if event.get("status", {}).get("type", {}).get("name") == "STATUS_IN_PROGRESS":
                        live_matches.append(event)
                return live_matches
        return []
```

## 🔧 Implementation Script

Let me create a script to set up real live matches:

```python
# Create: setup_live_api.py
import asyncio
import os
from datetime import datetime

async def setup_live_matches():
    """Setup real live match data"""
    
    # Option 1: API-Football (if you have key)
    api_key = os.getenv("FOOTBALL_API_KEY")
    if api_key:
        print("🏈 Using API-Football for live matches...")
        from backend.app.services.football_api import FootballAPIClient
        
        async with FootballAPIClient(api_key) as client:
            live_matches = await client.get_live_fixtures()
            print(f"Found {len(live_matches)} live matches")
            return live_matches
    
    # Option 2: Football-Data.org (free)
    football_data_token = os.getenv("FOOTBALL_DATA_TOKEN")
    if football_data_token:
        print("⚽ Using Football-Data.org for live matches...")
        # Implementation here
    
    # Option 3: ESPN (free, no key needed)
    print("📺 Using ESPN API for live matches...")
    # Implementation here
    
    return []

if __name__ == "__main__":
    asyncio.run(setup_live_matches())
```

## 🎯 Recommended Approach

**For Development/Testing:**
1. Use **Football-Data.org** (completely free, no credit card)
2. 10 requests/minute is enough for testing
3. Covers major European leagues

**For Production:**
1. Start with **API-Football free tier** (100 requests/day)
2. Upgrade to paid plan when you need more requests
3. Most comprehensive data and reliability

## 📝 Next Steps

1. **Choose your API** (I recommend Football-Data.org for free start)
2. **Get API credentials**
3. **Update your sync script** to use real API
4. **Test with live matches**

Would you like me to implement any of these options for you?