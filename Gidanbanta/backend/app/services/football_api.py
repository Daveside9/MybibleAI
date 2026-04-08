"""
Football API Client
Integrates with API-Football to fetch real match data
"""
import httpx
import asyncio
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class FootballAPIClient:
    """Client for API-Football integration"""
    
    def __init__(self, api_key: str, base_url: str = "https://api-football-v1.p.rapidapi.com/v3", rapidapi_host: str = "api-football-v1.p.rapidapi.com"):
        self.api_key = api_key
        self.base_url = base_url
        self.client: Optional[httpx.AsyncClient] = None
        # RapidAPI requires these specific headers
        self.headers = {
            "x-rapidapi-key": api_key,
            "x-rapidapi-host": rapidapi_host
        }
    
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
                    return None
                elif response.status_code >= 500:
                    # Server error, retry
                    if attempt < max_retries - 1:
                        await asyncio.sleep(2 ** attempt)  # Exponential backoff
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
    
    async def get_fixtures(
        self, 
        date_from: str, 
        date_to: str, 
        league_id: Optional[int] = None,
        timezone: str = "UTC"
    ) -> List[Dict]:
        """
        Fetch fixtures from API-Football
        
        Args:
            date_from: Start date (YYYY-MM-DD)
            date_to: End date (YYYY-MM-DD)
            league_id: Optional league ID to filter
            timezone: Timezone for match times
        
        Returns:
            List of fixture dictionaries
        """
        params = {
            "from": date_from,
            "to": date_to,
            "timezone": timezone
        }
        
        if league_id:
            params["league"] = league_id
        
        response = await self._make_request("fixtures", params)
        
        if response and "response" in response:
            return response["response"]
        
        return []
    
    async def get_live_fixtures(self) -> List[Dict]:
        """
        Fetch currently live fixtures
        
        Returns:
            List of live fixture dictionaries
        """
        params = {"live": "all"}
        response = await self._make_request("fixtures", params)
        
        if response and "response" in response:
            return response["response"]
        
        return []
    
    async def get_fixture_by_id(self, fixture_id: int) -> Optional[Dict]:
        """
        Fetch a specific fixture by ID
        
        Args:
            fixture_id: API-Football fixture ID
        
        Returns:
            Fixture dictionary or None
        """
        params = {"id": fixture_id}
        response = await self._make_request("fixtures", params)
        
        if response and "response" in response and len(response["response"]) > 0:
            return response["response"][0]
        
        return None
    
    async def get_odds(self, fixture_id: int) -> Optional[Dict]:
        """
        Fetch odds for a specific fixture
        
        Args:
            fixture_id: API-Football fixture ID
        
        Returns:
            Odds dictionary or None
        """
        params = {"fixture": fixture_id}
        response = await self._make_request("odds", params)
        
        if response and "response" in response and len(response["response"]) > 0:
            return response["response"][0]
        
        return None
    
    async def get_leagues(
        self, 
        season: Optional[int] = None,
        country: Optional[str] = None
    ) -> List[Dict]:
        """
        Fetch available leagues
        
        Args:
            season: Optional season year (e.g., 2024)
            country: Optional country name
        
        Returns:
            List of league dictionaries
        """
        params = {}
        if season:
            params["season"] = season
        if country:
            params["country"] = country
        
        response = await self._make_request("leagues", params)
        
        if response and "response" in response:
            return response["response"]
        
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
        
        required_fields = ["fixture", "teams", "league"]
        return all(field in data for field in required_fields)
    
    async def close(self):
        """Close the HTTP client"""
        if self.client:
            await self.client.aclose()
            self.client = None
