"""
Match Endpoints
List matches, join rooms, get match details
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.match import Match, MatchStatus, Team, League
from app.schemas.match import (
    MatchResponse,
    CalendarMatchResponse,
    CalendarResponse,
    LeagueWithCount,
    TeamResponse,
    LeagueResponse
)
from app.services.cache_service import cache_service
from app.middleware.rate_limit import limiter

router = APIRouter()

@router.get("/today", response_model=List[MatchResponse])
async def get_today_matches(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get today's matches (featured matches)"""
    matches = db.query(Match).filter(
        Match.is_featured == True,
        Match.status.in_([MatchStatus.SCHEDULED, MatchStatus.LIVE])
    ).order_by(Match.scheduled_at).limit(3).all()
    
    return [MatchResponse.from_orm(m) for m in matches]

@router.get("/{match_id}", response_model=MatchResponse)
async def get_match(
    match_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get match details"""
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found"
        )
    return MatchResponse.from_orm(match)


@router.get("/calendar/matches", response_model=CalendarResponse)
@limiter.limit("100/hour")
async def get_calendar_matches(
    request: Request,
    start_date: str = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: str = Query(..., description="End date (YYYY-MM-DD)"),
    league_id: Optional[int] = Query(None, description="Filter by league ID"),
    status: Optional[str] = Query(None, description="Filter by status"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get matches for calendar view with date range and optional filters
    """
    try:
        # Parse dates - set start to beginning of day and end to end of day
        start_dt = datetime.fromisoformat(start_date).replace(hour=0, minute=0, second=0, microsecond=0)
        end_dt = datetime.fromisoformat(end_date).replace(hour=23, minute=59, second=59, microsecond=999999)
        
        # Validate date range (max 14 days)
        if (end_dt - start_dt).days > 14:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Date range cannot exceed 14 days"
            )
        
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date format. Use YYYY-MM-DD"
        )
    
    # Skip cache for now to improve performance
    # cache_key_date = start_date if start_date == end_date else f"{start_date}_{end_date}"
    # cached_data = await cache_service.get_matches(cache_key_date, league_id)
    
    # if cached_data:
    #     # Return cached data
    #     return CalendarResponse(
    #         matches=[CalendarMatchResponse(**m) for m in cached_data["matches"]],
    #         total=len(cached_data["matches"]),
    #         cached=True,
    #         last_updated=datetime.fromisoformat(cached_data["cached_at"])
    #     )
    
    # Build query with eager loading
    query = db.query(Match).options(
        selectinload(Match.home_team_rel),
        selectinload(Match.away_team_rel),
        selectinload(Match.league)
    ).filter(
        Match.scheduled_at >= start_dt,
        Match.scheduled_at <= end_dt
    )
    
    # Apply filters
    if league_id:
        query = query.filter(Match.league_id == league_id)
    
    if status:
        try:
            status_enum = MatchStatus(status)
            query = query.filter(Match.status == status_enum)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status: {status}"
            )
    
    # Filter out mock matches - comprehensive approach
    # 1. Filter out matches with no external_id (clear mock indicator)
    query = query.filter(Match.external_id.isnot(None))
    query = query.filter(Match.external_id > 0)
    
    # 2. Filter out matches with scores for future dates (these are likely old/incorrect data)
    current_time = datetime.utcnow()
    if start_dt > current_time:  # If querying future dates
        query = query.filter(
            (Match.home_score.is_(None)) & (Match.away_score.is_(None))
        )
    
    # 3. For today's matches, exclude finished/expired matches (show only live and upcoming)
    today = datetime.now().date()
    if start_dt.date() == today and end_dt.date() == today:
        # For today, only show matches that are live, scheduled, or postponed (not finished)
        query = query.filter(
            Match.status.in_([MatchStatus.LIVE, MatchStatus.SCHEDULED, MatchStatus.POSTPONED])
        )
    
    # 3. Filter out known mock matches by name (backup filter)
    mock_match_names = [
        "Liverpool vs Chelsea",
        "Toulouse vs Eintracht Frankfurt", 
        "Chelsea vs Atletico Madrid",
        "Toulouse vs Slavia Prague",
        "Ajax vs PAOK",
        "Bologna vs Fiorentina",
        "Fulham vs Bournemouth",
        "Athletic Bilbao vs Sevilla"
    ]
    
    # Exclude known mock matches by name
    for mock_name in mock_match_names:
        query = query.filter(Match.title != mock_name)
    
    # Order by real matches first (external_id > 0), then by scheduled time
    query = query.order_by(
        Match.external_id.desc(),  # Real matches (external_id > 0) first
        Match.scheduled_at
    )
    
    matches = query.all()
    
    # Transform to response format
    calendar_matches = []
    matches_for_cache = []
    
    for match in matches:
        match_dict = {
            "id": match.id,
            "external_id": match.external_id,
            "home_team": match.home_team,
            "away_team": match.away_team,
            "home_team_data": TeamResponse.from_orm(match.home_team_rel).dict() if match.home_team_rel else None,
            "away_team_data": TeamResponse.from_orm(match.away_team_rel).dict() if match.away_team_rel else None,
            "league": LeagueResponse.from_orm(match.league).dict() if match.league else None,
            "scheduled_time": match.scheduled_at.isoformat(),
            "status": match.status.value,
            "home_score": match.home_score,
            "away_score": match.away_score,
            "home_odds": match.home_odds,
            "away_odds": match.away_odds,
            "draw_odds": match.draw_odds,
            "stream_url": match.stream_url
        }
        
        calendar_matches.append(CalendarMatchResponse(**match_dict))
        matches_for_cache.append(match_dict)
    
    # Skip cache saving for now to improve performance
    # await cache_service.set_matches(cache_key_date, matches_for_cache, league_id)
    
    return CalendarResponse(
        matches=calendar_matches,
        total=len(calendar_matches),
        cached=False,
        last_updated=datetime.utcnow()
    )


@router.get("/calendar/leagues", response_model=List[LeagueWithCount])
@limiter.limit("100/hour")
async def get_available_leagues(
    request: Request,
    start_date: str = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: str = Query(..., description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get available leagues for the date range with match counts
    """
    try:
        # Parse dates - set start to beginning of day and end to end of day
        start_dt = datetime.fromisoformat(start_date).replace(hour=0, minute=0, second=0, microsecond=0)
        end_dt = datetime.fromisoformat(end_date).replace(hour=23, minute=59, second=59, microsecond=999999)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date format. Use YYYY-MM-DD"
        )
    
    # Skip cache for now to improve performance
    # cached_data = await cache_service.get_leagues(start_date, end_date)
    
    # if cached_data:
    #     return [LeagueWithCount(**league) for league in cached_data["leagues"]]
    
    # Query leagues with match counts
    leagues_with_counts = db.query(
        League,
        func.count(Match.id).label('match_count')
    ).join(
        Match, Match.league_id == League.id
    ).filter(
        Match.scheduled_at >= start_dt,
        Match.scheduled_at <= end_dt
    ).group_by(
        League.id
    ).order_by(
        League.priority.desc(),
        League.name
    ).all()
    
    leagues_list = [
        LeagueWithCount(
            id=league.id,
            name=league.name,
            country=league.country,
            logo=league.logo,
            match_count=count
        )
        for league, count in leagues_with_counts
    ]
    
    # Skip cache saving for now to improve performance
    # leagues_for_cache = [league.dict() for league in leagues_list]
    # await cache_service.set_leagues(start_date, end_date, leagues_for_cache)
    
    return leagues_list
