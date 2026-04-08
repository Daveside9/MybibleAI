"""
Match & Match Room Models
Handles live matches and viewing rooms
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum, ForeignKey, Float, func
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.core.database import Base

class MatchStatus(str, enum.Enum):
    SCHEDULED = "scheduled"
    LIVE = "live"
    FINISHED = "finished"
    CANCELLED = "cancelled"
    POSTPONED = "postponed"
    SUSPENDED = "suspended"

class Match(Base):
    __tablename__ = "matches"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # API Integration
    external_id = Column(Integer, unique=True, nullable=True, index=True)  # API-Football ID
    
    # Match details
    title = Column(String, nullable=False)  # e.g., "Chelsea vs Arsenal"
    home_team = Column(String, nullable=False)
    away_team = Column(String, nullable=False)
    home_team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)
    away_team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)
    league_id = Column(Integer, ForeignKey("leagues.id"), nullable=True)
    
    home_score = Column(Integer, default=0)
    away_score = Column(Integer, default=0)
    
    # Betting odds
    home_odds = Column(Float, default=1.9)
    away_odds = Column(Float, default=1.9)
    draw_odds = Column(Float, default=3.0)
    
    # Streaming
    stream_url = Column(String, nullable=True)  # HLS stream URL
    stream_key = Column(String, nullable=True)  # Secret key for stream access
    
    # Status
    status = Column(Enum(MatchStatus), default=MatchStatus.SCHEDULED, nullable=False, index=True)
    is_featured = Column(Boolean, default=False)  # Show on dashboard
    
    # Timestamps
    scheduled_at = Column(DateTime(timezone=True), nullable=False, index=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    ended_at = Column(DateTime(timezone=True), nullable=True)
    last_synced = Column(DateTime(timezone=True), default=func.now())
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    home_team_rel = relationship("Team", foreign_keys=[home_team_id], back_populates="home_matches")
    away_team_rel = relationship("Team", foreign_keys=[away_team_id], back_populates="away_matches")
    league = relationship("League", back_populates="matches")
    rooms = relationship("MatchRoom", back_populates="match")
    transactions = relationship("Transaction", back_populates="match")
    
    def __repr__(self):
        return f"<Match {self.title}>"

class Team(Base):
    __tablename__ = "teams"
    
    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(Integer, unique=True, nullable=False, index=True)  # API-Football ID
    name = Column(String(100), nullable=False)
    logo = Column(String(500), nullable=True)
    country = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    
    # Relationships
    home_matches = relationship("Match", foreign_keys="Match.home_team_id", back_populates="home_team_rel")
    away_matches = relationship("Match", foreign_keys="Match.away_team_id", back_populates="away_team_rel")
    
    def __repr__(self):
        return f"<Team {self.name}>"


class League(Base):
    __tablename__ = "leagues"
    
    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(Integer, unique=True, nullable=False, index=True)  # API-Football ID
    name = Column(String(100), nullable=False)
    country = Column(String(50), nullable=False)
    logo = Column(String(500), nullable=True)
    priority = Column(Integer, default=0)  # For sorting popular leagues
    created_at = Column(DateTime(timezone=True), default=func.now())
    
    # Relationships
    matches = relationship("Match", back_populates="league")
    
    def __repr__(self):
        return f"<League {self.name}>"


class MatchRoom(Base):
    __tablename__ = "match_rooms"
    
    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Access control
    has_chat_access = Column(Boolean, default=False)  # Paid for chat
    free_messages_used = Column(Integer, default=0)   # Count of free messages
    
    # Timestamps
    joined_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    match = relationship("Match", back_populates="rooms")
    
    def __repr__(self):
        return f"<MatchRoom match_id={self.match_id} user_id={self.user_id}>"
