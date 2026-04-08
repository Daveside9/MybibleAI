"""
Match Room Endpoints
Join rooms, unlock chat, manage access
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_user
from app.core.config import settings
from app.models.user import User
from app.models.match import Match, MatchRoom, MatchStatus
from app.models.wallet import Wallet, Transaction, TransactionType, TransactionStatus

router = APIRouter()

@router.post("/join/{match_id}")
async def join_match_room(
    match_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Join a match room
    - Creates or updates MatchRoom entry
    - Returns chat access status and free messages left
    """
    # Check if match exists
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found"
        )
    
    # Check if match is live or scheduled
    if match.status not in [MatchStatus.LIVE, MatchStatus.SCHEDULED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Match is not available"
        )
    
    # Get or create match room entry
    room = db.query(MatchRoom).filter(
        MatchRoom.match_id == match_id,
        MatchRoom.user_id == current_user.id
    ).first()
    
    if not room:
        room = MatchRoom(
            match_id=match_id,
            user_id=current_user.id,
            has_chat_access=False,
            free_messages_used=0
        )
        db.add(room)
    
    # Update last active
    room.last_active = datetime.utcnow()
    db.commit()
    db.refresh(room)
    
    # Calculate free messages left
    free_messages_left = max(0, settings.FREE_MESSAGES_PER_MATCH - room.free_messages_used)
    
    return {
        "match_id": match_id,
        "has_chat_access": room.has_chat_access,
        "free_messages_left": free_messages_left,
        "can_send_message": room.has_chat_access or free_messages_left > 0
    }

@router.post("/unlock-chat/{match_id}")
async def unlock_chat(
    match_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Unlock chat for a match
    - Deducts 100 credits from wallet
    - Grants unlimited chat access for the match
    """
    # Check if user can purchase
    if not current_user.can_purchase:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You must be 18+ and KYC verified to purchase chat access"
        )
    
    # Check if match exists
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found"
        )
    
    # Get wallet
    wallet = db.query(Wallet).filter(Wallet.user_id == current_user.id).first()
    if not wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet not found"
        )
    
    # Check balance
    if wallet.balance < settings.CHAT_UNLOCK_PRICE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient balance. Need ₦{settings.CHAT_UNLOCK_PRICE}"
        )
    
    # Get or create match room
    room = db.query(MatchRoom).filter(
        MatchRoom.match_id == match_id,
        MatchRoom.user_id == current_user.id
    ).first()
    
    if not room:
        room = MatchRoom(
            match_id=match_id,
            user_id=current_user.id,
            has_chat_access=False,
            free_messages_used=0
        )
        db.add(room)
        db.flush()
    
    # Check if already unlocked
    if room.has_chat_access:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chat already unlocked for this match"
        )
    
    # Deduct from wallet
    wallet.balance -= settings.CHAT_UNLOCK_PRICE
    
    # Create transaction
    transaction = Transaction(
        user_id=current_user.id,
        type=TransactionType.CHAT_UNLOCK,
        amount=settings.CHAT_UNLOCK_PRICE,
        status=TransactionStatus.COMPLETED,
        match_id=match_id,
        description=f"Chat unlock for {match.title}",
        completed_at=datetime.utcnow()
    )
    db.add(transaction)
    
    # Grant chat access
    room.has_chat_access = True
    
    db.commit()
    db.refresh(wallet)
    
    return {
        "success": True,
        "message": "Chat unlocked successfully",
        "new_balance": wallet.balance,
        "has_chat_access": True
    }

@router.post("/send-message/{match_id}")
async def send_message(
    match_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Track message sending
    - Messages are now FREE and UNLIMITED for all users
    - Returns updated status
    """
    # Get match room
    room = db.query(MatchRoom).filter(
        MatchRoom.match_id == match_id,
        MatchRoom.user_id == current_user.id
    ).first()
    
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You haven't joined this match room"
        )
    
    # Messages are now FREE and UNLIMITED - no restrictions
    return {
        "success": True,
        "has_chat_access": True,
        "free_messages_left": 999999,  # Unlimited
        "message": "Messages are free and unlimited!"
    }
