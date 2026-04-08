"""
Football-Data.org API Client
Free football API with good coverage of major leagues
"""
import httpx
import asyncio
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class FootballDataClient:
    """Client for Football-Data.org API integration"""
    
    def __init__(self, api_key: str = None, base_url: str = "https://api.football-data.org/v4"):
        self.api_key = api_key
        self.base_url = base_url
        self.client: Optional[httpx.AsyncClient] = None
        
        # Headers for Football-Data.org
        self.headers = {}
        if api_key:
            self.headers["X-Auth-Token"] = api_key
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.client = httpx.AsyncClient(headers=self.headers, timeout=10.0)
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
            self.client = httpx.AsyncClient(headers=self.headers, timeout=10.0)
        
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
                    await asyncio.sleep(60)  # Wait 1 minute for rate limit reset
                    continue
                elif response.status_code == 403:
                    logger.error("API access forbidden - check your API key")
                    return None
                else:
                    logger.error(f"API request failed: {response.status_code} - {response.text}")
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
    
    async def get_competitions(self) -> List[Dict]:
        """
        Get available competitions/leagues
        
        Returns:
            List of competition dictionaries
        """
        response = await self._make_request("competitions")
        
        if response and "competitions" in response:
            return response["competitions"]
        
        return []
    
    async def get_matches(
        self, 
        competition_id: str = None,
        date_from: str = None,
        date_to: str = None
    ) -> List[Dict]:
        """
        Get matches with optional filters
        
        Args:
            competition_id: Competition ID to filter by
            date_from: Start date (YYYY-MM-DD)
            date_to: End date (YYYY-MM-DD)
        
        Returns:
            List of match dictionaries
        """
        endpoint = "matches"
        params = {}
        
        if competition_id:
            endpoint = f"competitions/{competition_id}/matches"
        
        if date_from:
            params["dateFrom"] = date_from
        if date_to:
            params["dateTo"] = date_to
        
        response = await self._make_request(endpoint, params)
        
        if response and "matches" in response:
            return response["matches"]
        
        return []
    
    async def get_competition_matches(
        self, 
        competition_code: str,
        date_from: str = None,
        date_to: str = None
    ) -> List[Dict]:
        """
        Get matches for a specific competition
        
        Args:
            competition_code: Competition code (e.g., 'PL', 'PD', 'SA')
            date_from: Start date (YYYY-MM-DD)
            date_to: End date (YYYY-MM-DD)
        
        Returns:
            List of match dictionaries
        """
        endpoint = f"competitions/{competition_code}/matches"
        params = {}
        
        if date_from:
            params["dateFrom"] = date_from
        if date_to:
            params["dateTo"] = date_to
        
        response = await self._make_request(endpoint, params)
        
        if response and "matches" in response:
            return response["matches"]
        
        return []
    
    async def get_todays_matches(self) -> List[Dict]:
        """
        Get today's matches across all competitions
        
        Returns:
            List of today's match dictionaries
        """
        today = datetime.now().date().isoformat()
        
        response = await self._make_request("matches", {"dateFrom": today, "dateTo": today})
        
        if response and "matches" in response:
            return response["matches"]
        
        return []
    
    async def get_team_matches(self, team_id: int) -> List[Dict]:
        """
        Get matches for a specific team
        
        Args:
            team_id: Team ID
        
        Returns:
            List of team match dictionaries
        """
        response = await self._make_request(f"teams/{team_id}/matches")
        
        if response and "matches" in response:
            return response["matches"]
        
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
        
        # Football-Data.org has consistent structure
        return "matches" in data or "competitions" in data or "teams" in data
    
    async def close(self):
        """Close the HTTP client"""
        if self.client:
            await self.client.aclose()
            self.client = None


# Competition codes for major leagues in Football-Data.org
FOOTBALL_DATA_COMPETITIONS = {
    "Premier League": "PL",
    "La Liga": "PD", 
    "Serie A": "SA",
    "Bundesliga": "BL1",
    "Ligue 1": "FL1",
    "Champions League": "CL",
    "Europa League": "EL"
}