"""
Admin Endpoints
Match management, user management, platform control
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User, UserRole
from app.models.match import Match, MatchStatus
from app.models.wallet import Wallet
from app.schemas.match import MatchCreate, MatchResponse
from app.services.match_service import get_match_service

router = APIRouter()

def require_admin(current_user: User = Depends(get_current_user)):
    """Dependency to require admin role"""
    if current_user.role not in [UserRole.ADMIN, UserRole.MODERATOR]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

@router.post("/matches", response_model=MatchResponse)
async def create_match(
    match_data: MatchCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """
    Create a new match
    Admin only
    """
    new_match = Match(
        title=match_data.title,
        home_team=match_data.home_team,
        away_team=match_data.away_team,
        scheduled_at=match_data.scheduled_at,
        stream_url=match_data.stream_url,
        is_featured=match_data.is_featured,
        status=MatchStatus.SCHEDULED
    )
    
    db.add(new_match)
    db.commit()
    db.refresh(new_match)
    
    return MatchResponse.from_orm(new_match)

@router.put("/matches/{match_id}/status")
async def update_match_status(
    match_id: int,
    status: str,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """
    Update match status (scheduled, live, finished, cancelled)
    Admin only
    """
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found"
        )
    
    try:
        match.status = MatchStatus(status)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Must be one of: {[s.value for s in MatchStatus]}"
        )
    
    if status == 'live' and not match.started_at:
        match.started_at = datetime.utcnow()
    elif status == 'finished' and not match.ended_at:
        match.ended_at = datetime.utcnow()
    
    db.commit()
    db.refresh(match)
    
    return MatchResponse.from_orm(match)

@router.put("/matches/{match_id}/score")
async def update_match_score(
    match_id: int,
    home_score: int,
    away_score: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """
    Update match score
    Admin only
    """
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found"
        )
    
    match.home_score = home_score
    match.away_score = away_score
    
    db.commit()
    db.refresh(match)
    
    return MatchResponse.from_orm(match)

@router.get("/matches", response_model=List[MatchResponse])
async def list_all_matches(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
    skip: int = 0,
    limit: int = 50
):
    """
    List all matches (including past)
    Admin only
    """
    matches = db.query(Match).order_by(
        Match.scheduled_at.desc()
    ).offset(skip).limit(limit).all()
    
    return [MatchResponse.from_orm(m) for m in matches]

@router.get("/stats")
async def get_platform_stats(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """
    Get platform statistics
    Admin only
    """
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    total_matches = db.query(Match).count()
    live_matches = db.query(Match).filter(Match.status == MatchStatus.LIVE).count()
    
    # Calculate total wallet balance
    total_balance = db.query(Wallet).with_entities(
        db.func.sum(Wallet.balance)
    ).scalar() or 0
    
    return {
        "users": {
            "total": total_users,
            "active": active_users,
            "banned": total_users - active_users
        },
        "matches": {
            "total": total_matches,
            "live": live_matches
        },
        "wallet": {
            "total_balance": float(total_balance)
        }
    }

@router.post("/users/{user_id}/ban")
async def ban_user(
    user_id: int,
    reason: str,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """
    Ban a user
    Admin only
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user.role == UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot ban admin users"
        )
    
    user.is_banned = True
    user.is_active = False
    db.commit()
    
    return {
        "success": True,
        "message": f"User {user.username} has been banned",
        "reason": reason
    }

@router.post("/users/{user_id}/unban")
async def unban_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """
    Unban a user
    Admin only
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.is_banned = False
    user.is_active = True
    db.commit()
    
    return {
        "success": True,
        "message": f"User {user.username} has been unbanned"
    }


@router.post("/matches/sync")
async def sync_matches_from_api(
    date_from: str = None,
    date_to: str = None,
    league_id: int = None,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """
    Manually trigger match synchronization from Football API
    Admin only
    
    If no dates provided, syncs next 14 days
    """
    match_service = get_match_service(db)
    
    if date_from and date_to:
        stats = await match_service.sync_matches(date_from, date_to, league_id)
    else:
        stats = await match_service.sync_next_14_days()
    
    return {
        "success": True,
        "message": "Match synchronization completed",
        "stats": stats
    }


@router.post("/matches/sync-live")
async def sync_live_matches(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """
    Manually trigger live match updates
    Admin only
    """
    match_service = get_match_service(db)
    stats = await match_service.update_live_matches()
    
    return {
        "success": True,
        "message": "Live matches updated",
        "stats": stats
    }
