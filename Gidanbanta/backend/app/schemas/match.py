"""
Match Schemas
Request/Response models for match operations
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class TeamResponse(BaseModel):
    id: int
    name: str
    logo: Optional[str] = None
    
    class Config:
        from_attributes = True


class LeagueResponse(BaseModel):
    id: int
    name: str
    country: str
    logo: Optional[str] = None
    
    class Config:
        from_attributes = True


class LeagueWithCount(BaseModel):
    id: int
    name: str
    country: str
    logo: Optional[str] = None
    match_count: int


class MatchCreate(BaseModel):
    title: str
    home_team: str
    away_team: str
    scheduled_at: datetime
    stream_url: Optional[str] = None
    is_featured: bool = False


class MatchResponse(BaseModel):
    id: int
    external_id: Optional[int] = None
    title: str
    home_team: str
    away_team: str
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    status: str
    is_featured: bool
    scheduled_at: datetime
    started_at: Optional[datetime]
    ended_at: Optional[datetime]
    stream_url: Optional[str] = None
    
    class Config:
        from_attributes = True


class CalendarMatchResponse(BaseModel):
    id: int
    external_id: Optional[int] = None
    home_team: str
    away_team: str
    home_team_data: Optional[TeamResponse] = None
    away_team_data: Optional[TeamResponse] = None
    league: Optional[LeagueResponse] = None
    scheduled_time: datetime
    status: str
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    home_odds: float
    away_odds: float
    draw_odds: float
    stream_url: Optional[str] = None
    
    class Config:
        from_attributes = True


class CalendarResponse(BaseModel):
    matches: List[CalendarMatchResponse]
    total: int
    cached: bool
    last_updated: datetime

class MatchRoomJoin(BaseModel):
    match_id: int

class ChatMessageCreate(BaseModel):
    match_id: int
    content: str
    type: str = "text"
