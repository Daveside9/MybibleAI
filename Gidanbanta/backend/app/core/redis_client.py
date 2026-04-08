"""
Redis Client Configuration
For caching, sessions, and real-time data
"""
import redis
from app.core.config import settings

# Main Redis client
redis_client = redis.from_url(
    settings.REDIS_URL,
    decode_responses=True
)

# Chat-specific Redis client
chat_redis = redis.from_url(
    settings.REDIS_URL,
    db=settings.REDIS_CHAT_DB,
    decode_responses=True
)

# Session Redis client
session_redis = redis.from_url(
    settings.REDIS_URL,
    db=settings.REDIS_SESSION_DB,
    decode_responses=True
)

def get_redis():
    """Dependency for Redis client"""
    return redis_client
