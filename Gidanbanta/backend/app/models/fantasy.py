from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class FantasyPlayer(Base):
    """Fantasy player model representing real football players"""
    __tablename__ = "fantasy_players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    position = Column(String, nullable=False)  # GK, DEF, MID, FWD
    team = Column(String, nullable=False, index=True)
    cost = Column(Float, nullable=False)  # Cost in fantasy coins
    points = Column(Integer, default=0)  # Total fantasy points
    goals = Column(Integer, default=0)
    assists = Column(Integer, default=0)
    clean_sheets = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    team_players = relationship("TeamPlayer", back_populates="player")


class FantasyTeam(Base):
    """Fantasy team model for user-created teams"""
    __tablename__ = "fantasy_teams"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    name = Column(String, nullable=False)
    formation = Column(String, nullable=False)  # e.g., "4-3-3"
    budget_remaining = Column(Float, default=100.0)
    total_points = Column(Integer, default=0)
    captain_player_id = Column(Integer, ForeignKey("fantasy_players.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    # user = relationship("User", back_populates="fantasy_team")
    captain = relationship("FantasyPlayer", foreign_keys=[captain_player_id])
    team_players = relationship("TeamPlayer", back_populates="team", cascade="all, delete-orphan")


class TeamPlayer(Base):
    """Association table for fantasy teams and players"""
    __tablename__ = "team_players"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("fantasy_teams.id"), nullable=False)
    player_id = Column(Integer, ForeignKey("fantasy_players.id"), nullable=False)
    is_captain = Column(Boolean, default=False)
    position_in_formation = Column(Integer, nullable=False)  # 1-11
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    team = relationship("FantasyTeam", back_populates="team_players")
    player = relationship("FantasyPlayer", back_populates="team_players")
