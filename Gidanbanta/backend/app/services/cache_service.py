"""
Cache Service
Redis caching layer for match data
"""
import json
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from redis import Redis

from app.core.redis_client import redis_client

logger = logging.getLogger(__name__)


class CacheService:
    """Service for caching match data in Redis"""
    
    def __init__(self, redis_client: Redis = redis_client):
        self.redis = redis_client
        
        # TTL configurations (in seconds)
        self.TTL_SCHEDULED = 1800  # 30 minutes
        self.TTL_LIVE = 300  # 5 minutes
        self.TTL_FINISHED = 86400  # 24 hours
        self.TTL_LEAGUES = 3600  # 1 hour
    
    def _make_key(self, prefix: str, *args) -> str:
        """Generate cache key"""
        parts = [prefix] + [str(arg) for arg in args]
        return ":".join(parts)
    
    async def get_matches(
        self, 
        date: str, 
        league_id: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve cached matches for a date
        
        Args:
            date: Date string (YYYY-MM-DD)
            league_id: Optional league filter
        
        Returns:
            Cached match data or None
        """
        try:
            if not self.redis:
                return None
                
            if league_id:
                key = self._make_key("matches", "date", date, "league", league_id)
            else:
                key = self._make_key("matches", "date", date)
            
            cached_data = self.redis.get(key)
            
            if cached_data:
                logger.info(f"Cache hit for key: {key}")
                return json.loads(cached_data)
            
            logger.info(f"Cache miss for key: {key}")
            return None
            
        except Exception as e:
            logger.warning(f"Redis not available, skipping cache: {e}")
            return None
    
    async def set_matches(
        self, 
        date: str, 
        matches: List[Dict[str, Any]], 
        league_id: Optional[int] = None,
        ttl: Optional[int] = None
    ) -> bool:
        """
        Cache matches for a date
        
        Args:
            date: Date string (YYYY-MM-DD)
            matches: List of match dictionaries
            league_id: Optional league filter
            ttl: Time to live in seconds (optional)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.redis:
                return False
                
            if league_id:
                key = self._make_key("matches", "date", date, "league", league_id)
            else:
                key = self._make_key("matches", "date", date)
            
            # Use default TTL if not provided
            if ttl is None:
                ttl = self.TTL_SCHEDULED
            
            # Prepare cache data
            cache_data = {
                "matches": matches,
                "cached_at": datetime.utcnow().isoformat(),
                "date": date,
                "league_id": league_id
            }
            
            # Store in Redis
            self.redis.setex(
                key,
                ttl,
                json.dumps(cache_data, default=str)
            )
            
            logger.info(f"Cached {len(matches)} matches for key: {key} (TTL: {ttl}s)")
            return True
            
        except Exception as e:
            logger.warning(f"Redis not available, skipping cache: {e}")
            return False
    
    async def get_live_matches(self) -> Optional[Dict[str, Any]]:
        """
        Retrieve cached live matches
        
        Returns:
            Cached live match data or None
        """
        try:
            key = self._make_key("matches", "live")
            cached_data = self.redis.get(key)
            
            if cached_data:
                logger.info("Cache hit for live matches")
                return json.loads(cached_data)
            
            logger.info("Cache miss for live matches")
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving live matches from cache: {e}")
            return None
    
    async def set_live_matches(
        self, 
        matches: List[Dict[str, Any]]
    ) -> bool:
        """
        Cache live matches
        
        Args:
            matches: List of live match dictionaries
        
        Returns:
            True if successful, False otherwise
        """
        try:
            key = self._make_key("matches", "live")
            
            cache_data = {
                "matches": matches,
                "cached_at": datetime.utcnow().isoformat()
            }
            
            self.redis.setex(
                key,
                self.TTL_LIVE,
                json.dumps(cache_data, default=str)
            )
            
            logger.info(f"Cached {len(matches)} live matches (TTL: {self.TTL_LIVE}s)")
            return True
            
        except Exception as e:
            logger.error(f"Error caching live matches: {e}")
            return False
    
    async def get_leagues(
        self, 
        start_date: str, 
        end_date: str
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve cached leagues for date range
        
        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
        
        Returns:
            Cached league data or None
        """
        try:
            if not self.redis:
                return None
                
            key = self._make_key("leagues", "range", start_date, end_date)
            cached_data = self.redis.get(key)
            
            if cached_data:
                logger.info(f"Cache hit for leagues: {key}")
                return json.loads(cached_data)
            
            logger.info(f"Cache miss for leagues: {key}")
            return None
            
        except Exception as e:
            logger.warning(f"Redis not available, skipping cache: {e}")
            return None
    
    async def set_leagues(
        self, 
        start_date: str, 
        end_date: str, 
        leagues: List[Dict[str, Any]]
    ) -> bool:
        """
        Cache leagues for date range
        
        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            leagues: List of league dictionaries
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.redis:
                return False
                
            key = self._make_key("leagues", "range", start_date, end_date)
            
            cache_data = {
                "leagues": leagues,
                "cached_at": datetime.utcnow().isoformat(),
                "start_date": start_date,
                "end_date": end_date
            }
            
            self.redis.setex(
                key,
                self.TTL_LEAGUES,
                json.dumps(cache_data, default=str)
            )
            
            logger.info(f"Cached {len(leagues)} leagues for key: {key}")
            return True
            
        except Exception as e:
            logger.warning(f"Redis not available, skipping cache: {e}")
            return False
    
    async def invalidate_date(self, date: str) -> bool:
        """
        Invalidate cache for a specific date
        
        Args:
            date: Date string (YYYY-MM-DD)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Find all keys for this date
            pattern = self._make_key("matches", "date", date, "*")
            keys = self.redis.keys(pattern)
            
            if keys:
                self.redis.delete(*keys)
                logger.info(f"Invalidated {len(keys)} cache keys for date: {date}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error invalidating cache for date {date}: {e}")
            return False
    
    async def invalidate_all_matches(self) -> bool:
        """
        Invalidate all match caches
        
        Returns:
            True if successful, False otherwise
        """
        try:
            pattern = self._make_key("matches", "*")
            keys = self.redis.keys(pattern)
            
            if keys:
                self.redis.delete(*keys)
                logger.info(f"Invalidated {len(keys)} match cache keys")
            
            return True
            
        except Exception as e:
            logger.error(f"Error invalidating all match caches: {e}")
            return False
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics
        
        Returns:
            Dictionary with cache stats
        """
        try:
            info = self.redis.info()
            
            return {
                "connected": True,
                "used_memory": info.get("used_memory_human", "N/A"),
                "total_keys": self.redis.dbsize(),
                "hits": info.get("keyspace_hits", 0),
                "misses": info.get("keyspace_misses", 0),
                "hit_rate": self._calculate_hit_rate(
                    info.get("keyspace_hits", 0),
                    info.get("keyspace_misses", 0)
                )
            }
        except Exception as e:
            logger.error(f"Error getting cache stats: {e}")
            return {
                "connected": False,
                "error": str(e)
            }
    
    def _calculate_hit_rate(self, hits: int, misses: int) -> float:
        """Calculate cache hit rate percentage"""
        total = hits + misses
        if total == 0:
            return 0.0
        return round((hits / total) * 100, 2)


# Global cache service instance
cache_service = CacheService()
