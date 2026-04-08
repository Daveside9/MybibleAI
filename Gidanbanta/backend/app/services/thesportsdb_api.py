"""
TheSportsDB API Client
Free football API integration for real match data
"""
import httpx
import asyncio
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class TheSportsDBClient:
    """Client for TheSportsDB V1 API integration"""
    
    def __init__(self, base_url: str = "https://www.thesportsdb.com/api/v1/json"):
        self.base_url = base_url
        self.client: Optional[httpx.AsyncClient] = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.client = httpx.AsyncClient(timeout=10.0)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.client:
            await self.client.aclose()
    
    async def _make_request(
        self, 
        endpoint: str, 
        params: Dict = None,
        max_retries: int = 3
    ) -> Optional[Dict]:
        """Make API request with retry logic"""
        if not self.client:
            self.client = httpx.AsyncClient(timeout=10.0)
        
        url = f"{self.base_url}/{endpoint}"
        
        for attempt in range(max_retries):
            try:
                response = await self.client.get(url, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    return data
                elif response.status_code == 429:
                    # Rate limit exceeded
                    logger.warning("API rate limit exceeded")
                    await asyncio.sleep(2 ** attempt)
                    continue
                else:
                    logger.error(f"API request failed: {response.status_code}")
                    return None
            except httpx.TimeoutException:
                logger.warning(f"API request timeout (attempt {attempt + 1}/{max_retries})")
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                    continue
            except Exception as e:
                logger.error(f"API request error: {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                    continue
        
        return None
    
    async def get_leagues(self, country: str = "England") -> List[Dict]:
        """
        Get leagues for a specific country
        
        Args:
            country: Country name (e.g., "England", "Spain", "Italy")
        
        Returns:
            List of league dictionaries
        """
        response = await self._make_request(f"search_all_leagues.php?c={country}")
        
        if response and "countrys" in response:
            return response["countrys"]
        
        return []
    
    async def get_league_fixtures(
        self, 
        league_id: str,
        season: str = "2024-2025"
    ) -> List[Dict]:
        """
        Get fixtures for a specific league and season
        
        Args:
            league_id: League ID from TheSportsDB
            season: Season string (e.g., "2024-2025")
        
        Returns:
            List of fixture dictionaries
        """
        response = await self._make_request(f"eventsseason.php?id={league_id}&s={season}")
        
        if response and "events" in response:
            return response["events"]
        
        return []
    
    async def get_next_fixtures(self, league_id: str, count: int = 15) -> List[Dict]:
        """
        Get next fixtures for a league
        
        Args:
            league_id: League ID from TheSportsDB
            count: Number of fixtures to return
        
        Returns:
            List of upcoming fixture dictionaries
        """
        response = await self._make_request(f"eventsnextleague.php?id={league_id}")
        
        if response and "events" in response:
            return response["events"][:count]
        
        return []
    
    async def get_last_fixtures(self, league_id: str, count: int = 15) -> List[Dict]:
        """
        Get recent fixtures for a league
        
        Args:
            league_id: League ID from TheSportsDB
            count: Number of fixtures to return
        
        Returns:
            List of recent fixture dictionaries
        """
        response = await self._make_request(f"eventspastleague.php?id={league_id}")
        
        if response and "events" in response:
            return response["events"][:count]
        
        return []
    
    async def get_live_scores(self) -> List[Dict]:
        """
        Get live scores (limited in free version)
        
        Returns:
            List of live match dictionaries
        """
        response = await self._make_request("latestscore.php")
        
        if response and "events" in response:
            return response["events"]
        
        return []
    
    async def search_team(self, team_name: str) -> Optional[Dict]:
        """
        Search for a team by name
        
        Args:
            team_name: Team name to search for
        
        Returns:
            Team dictionary or None
        """
        response = await self._make_request(f"searchteams.php?t={team_name}")
        
        if response and "teams" in response and len(response["teams"]) > 0:
            return response["teams"][0]
        
        return None
    
    async def get_team_fixtures(self, team_id: str) -> List[Dict]:
        """
        Get fixtures for a specific team
        
        Args:
            team_id: Team ID from TheSportsDB
        
        Returns:
            List of team fixture dictionaries
        """
        response = await self._make_request(f"eventsnext.php?id={team_id}")
        
        if response and "events" in response:
            return response["events"]
        
        return []
    
    def validate_response(self, data: Dict) -> bool:
        """
        Validate API response structure
        
        Args:
            data: Response data from API
        
        Returns:
            True if valid, False otherwise
        """
        if not data:
            return False
        
        # TheSportsDB has different structure than API-Football
        return "events" in data or "teams" in data or "countrys" in data
    
    async def close(self):
        """Close the HTTP client"""
        if self.client:
            await self.client.aclose()
            self.client = None


# League IDs for major competitions in TheSportsDB
THESPORTSDB_LEAGUES = {
    "Premier League": "4328",
    "La Liga": "4335", 
    "Serie A": "4332",
    "Bundesliga": "4331",
    "Ligue 1": "4334",
    "Champions League": "4480",
    "Europa League": "4481"
}