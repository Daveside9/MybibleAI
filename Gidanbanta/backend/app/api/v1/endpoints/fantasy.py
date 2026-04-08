from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.fantasy import FantasyTeam, FantasyPlayer, TeamPlayer
from app.schemas.fantasy import (
    FantasyTeam as FantasyTeamSchema,
    FantasyTeamCreate,
    FantasyTeamUpdate,
    FantasyPlayer as FantasyPlayerSchema,
    LeaderboardEntry,
    PlayerFilter
)

router = APIRouter()

# Formation requirements
FORMATION_RULES = {
    "4-3-3": {"GK": 1, "DEF": 4, "MID": 3, "FWD": 3},
    "4-4-2": {"GK": 1, "DEF": 4, "MID": 4, "FWD": 2},
    "3-5-2": {"GK": 1, "DEF": 3, "MID": 5, "FWD": 2},
    "3-4-3": {"GK": 1, "DEF": 3, "MID": 4, "FWD": 3},
}

INITIAL_BUDGET = 200.0


def validate_team_composition(players: List[FantasyPlayer], formation: str) -> tuple[bool, str]:
    """Validate team composition against formation rules"""
    if formation not in FORMATION_RULES:
        return False, f"Invalid formation: {formation}"
    
    # Count players by position
    position_counts = {"GK": 0, "DEF": 0, "MID": 0, "FWD": 0}
    total_cost = 0.0
    
    for player in players:
        position_counts[player.position] += 1
        total_cost += player.cost
    
    # Check formation requirements
    required = FORMATION_RULES[formation]
    for position, count in required.items():
        if position_counts[position] != count:
            return False, f"Formation {formation} requires {count} {position}, but got {position_counts[position]}"
    
    # Check budget
    if total_cost > INITIAL_BUDGET:
        return False, f"Total cost {total_cost} exceeds budget {INITIAL_BUDGET}"
    
    return True, "Valid"


@router.get("/players", response_model=List[FantasyPlayerSchema])
def get_players(
    position: Optional[str] = Query(None, regex="^(GK|DEF|MID|FWD)$"),
    team: Optional[str] = None,
    min_cost: Optional[float] = None,
    max_cost: Optional[float] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get list of available fantasy players with optional filtering"""
    query = db.query(FantasyPlayer)
    
    if position:
        query = query.filter(FantasyPlayer.position == position)
    if team:
        query = query.filter(FantasyPlayer.team == team)
    if min_cost is not None:
        query = query.filter(FantasyPlayer.cost >= min_cost)
    if max_cost is not None:
        query = query.filter(FantasyPlayer.cost <= max_cost)
    if search:
        query = query.filter(FantasyPlayer.name.ilike(f"%{search}%"))
    
    players = query.order_by(FantasyPlayer.points.desc()).all()
    return players


@router.get("/players/{player_id}", response_model=FantasyPlayerSchema)
def get_player(
    player_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get details of a specific fantasy player"""
    player = db.query(FantasyPlayer).filter(FantasyPlayer.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


@router.get("/team", response_model=FantasyTeamSchema)
def get_my_team(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user's fantasy team"""
    team = db.query(FantasyTeam).filter(FantasyTeam.user_id == current_user.id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Fantasy team not found")
    return team


@router.post("/team", response_model=FantasyTeamSchema, status_code=201)
def create_team(
    team_data: FantasyTeamCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new fantasy team"""
    # Check if user already has a team
    existing_team = db.query(FantasyTeam).filter(FantasyTeam.user_id == current_user.id).first()
    if existing_team:
        raise HTTPException(status_code=400, detail="User already has a fantasy team")
    
    # Validate player count
    if len(team_data.player_ids) != 11:
        raise HTTPException(status_code=400, detail="Team must have exactly 11 players")
    
    # Fetch players
    players = db.query(FantasyPlayer).filter(FantasyPlayer.id.in_(team_data.player_ids)).all()
    if len(players) != 11:
        missing_ids = set(team_data.player_ids) - set(p.id for p in players)
        raise HTTPException(status_code=400, detail=f"One or more players not found: {missing_ids}")
    
    # Validate team composition
    is_valid, message = validate_team_composition(players, team_data.formation)
    if not is_valid:
        raise HTTPException(status_code=400, detail=message)
    
    # Validate captain
    if team_data.captain_player_id not in team_data.player_ids:
        raise HTTPException(status_code=400, detail="Captain must be one of the selected players")
    
    # Calculate budget remaining
    total_cost = sum(player.cost for player in players)
    budget_remaining = INITIAL_BUDGET - total_cost
    
    # Create team
    new_team = FantasyTeam(
        user_id=current_user.id,
        name=team_data.name,
        formation=team_data.formation,
        budget_remaining=budget_remaining,
        captain_player_id=team_data.captain_player_id,
        total_points=0
    )
    db.add(new_team)
    db.flush()
    
    # Add players to team
    for idx, player_id in enumerate(team_data.player_ids, start=1):
        team_player = TeamPlayer(
            team_id=new_team.id,
            player_id=player_id,
            is_captain=(player_id == team_data.captain_player_id),
            position_in_formation=idx
        )
        db.add(team_player)
    
    db.commit()
    db.refresh(new_team)
    return new_team


@router.put("/team", response_model=FantasyTeamSchema)
def update_team(
    team_data: FantasyTeamUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update user's fantasy team"""
    team = db.query(FantasyTeam).filter(FantasyTeam.user_id == current_user.id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Fantasy team not found")
    
    # Update basic fields
    if team_data.name:
        team.name = team_data.name
    if team_data.formation:
        team.formation = team_data.formation
    
    # Update players if provided
    if team_data.player_ids:
        if len(team_data.player_ids) != 11:
            raise HTTPException(status_code=400, detail="Team must have exactly 11 players")
        
        # Fetch players
        players = db.query(FantasyPlayer).filter(FantasyPlayer.id.in_(team_data.player_ids)).all()
        if len(players) != 11:
            raise HTTPException(status_code=400, detail="One or more players not found")
        
        # Validate team composition
        is_valid, message = validate_team_composition(players, team.formation)
        if not is_valid:
            raise HTTPException(status_code=400, detail=message)
        
        # Delete existing team players
        db.query(TeamPlayer).filter(TeamPlayer.team_id == team.id).delete()
        
        # Add new players
        for idx, player_id in enumerate(team_data.player_ids, start=1):
            team_player = TeamPlayer(
                team_id=team.id,
                player_id=player_id,
                is_captain=(player_id == team_data.captain_player_id),
                position_in_formation=idx
            )
            db.add(team_player)
        
        # Update budget
        total_cost = sum(player.cost for player in players)
        team.budget_remaining = INITIAL_BUDGET - total_cost
    
    # Update captain
    if team_data.captain_player_id:
        team.captain_player_id = team_data.captain_player_id
    
    db.commit()
    db.refresh(team)
    return team


@router.delete("/team", status_code=204)
def delete_team(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete user's fantasy team"""
    team = db.query(FantasyTeam).filter(FantasyTeam.user_id == current_user.id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Fantasy team not found")
    
    db.delete(team)
    db.commit()
    return None


@router.get("/leaderboard", response_model=List[LeaderboardEntry])
def get_leaderboard(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get fantasy football leaderboard"""
    teams = db.query(FantasyTeam, User).join(User).order_by(FantasyTeam.total_points.desc()).limit(limit).all()
    
    leaderboard = []
    for rank, (team, user) in enumerate(teams, start=1):
        leaderboard.append(LeaderboardEntry(
            rank=rank,
            team_name=team.name,
            username=user.username,
            total_points=team.total_points,
            formation=team.formation
        ))
    
    return leaderboard
