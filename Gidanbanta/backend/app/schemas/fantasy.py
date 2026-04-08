from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


# Fantasy Player Schemas
class FantasyPlayerBase(BaseModel):
    name: str
    position: str = Field(..., pattern="^(GK|DEF|MID|FWD)$")
    team: str
    cost: float = Field(..., ge=5.0, le=15.0)


class FantasyPlayerCreate(FantasyPlayerBase):
    pass


class FantasyPlayer(FantasyPlayerBase):
    id: int
    points: int = 0
    goals: int = 0
    assists: int = 0
    clean_sheets: int = 0
    created_at: datetime

    class Config:
        from_attributes = True


# Team Player Schemas
class TeamPlayerBase(BaseModel):
    player_id: int
    is_captain: bool = False
    position_in_formation: int = Field(..., ge=1, le=11)


class TeamPlayerCreate(TeamPlayerBase):
    pass


class TeamPlayer(TeamPlayerBase):
    id: int
    team_id: int
    player: FantasyPlayer
    created_at: datetime

    class Config:
        from_attributes = True


# Fantasy Team Schemas
class FantasyTeamBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    formation: str = Field(..., pattern="^(4-3-3|4-4-2|3-5-2|3-4-3)$")


class FantasyTeamCreate(FantasyTeamBase):
    player_ids: List[int] = Field(..., min_length=11, max_length=11)
    captain_player_id: int


class FantasyTeamUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=50)
    formation: Optional[str] = Field(None, pattern="^(4-3-3|4-4-2|3-5-2|3-4-3)$")
    player_ids: Optional[List[int]] = Field(None, min_length=11, max_length=11)
    captain_player_id: Optional[int] = None


class FantasyTeam(FantasyTeamBase):
    id: int
    user_id: int
    budget_remaining: float
    total_points: int
    captain_player_id: Optional[int]
    team_players: List[TeamPlayer] = []
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


# Leaderboard Schema
class LeaderboardEntry(BaseModel):
    rank: int
    team_name: str
    username: str
    total_points: int
    formation: str

    class Config:
        from_attributes = True


# Player Filter Schema
class PlayerFilter(BaseModel):
    position: Optional[str] = Field(None, pattern="^(GK|DEF|MID|FWD)$")
    team: Optional[str] = None
    min_cost: Optional[float] = Field(None, ge=0)
    max_cost: Optional[float] = Field(None, le=100)
    search: Optional[str] = None
