"""
Application Configuration
Loads environment variables and provides settings
"""
from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "MatchHang"
    DEBUG: bool = True
    SECRET_KEY: str
    API_VERSION: str = "v1"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 4000
    
    # Database
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10
    
    # Redis
    REDIS_URL: str
    REDIS_CHAT_DB: int = 1
    REDIS_SESSION_DB: int = 2
    
    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # Payment Providers
    OPAY_API_KEY: str = ""
    OPAY_MERCHANT_ID: str = ""
    PALMPAY_API_KEY: str = ""
    MONIEPOINT_API_KEY: str = ""
    
    # Streaming
    HLS_SECRET_KEY: str
    STREAM_TOKEN_EXPIRE_HOURS: int = 3
    
    # Football API
    FOOTBALL_API_KEY: str = ""
    FOOTBALL_API_BASE_URL: str = "https://api-football-v1.p.rapidapi.com/v3"
    RAPIDAPI_HOST: str = "api-football-v1.p.rapidapi.com"
    
    # Football Data API (free)
    FOOTBALL_DATA_TOKEN: str = ""
    
    # Moderation
    MODERATION_API_KEY: str = ""
    AUTO_MODERATE: bool = True
    
    # Celery
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    
    # App Settings
    CHAT_UNLOCK_PRICE: int = 0  # Free chat
    FREE_MESSAGES_PER_MATCH: int = 999999  # Unlimited messages
    MIN_AGE: int = 18
    KYC_REQUIRED_FOR_PURCHASE: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
