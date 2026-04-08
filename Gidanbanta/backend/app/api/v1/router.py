"""
API v1 Router
Combines all API endpoints
"""
from fastapi import APIRouter
from app.api.v1.endpoints import auth, wallet, matches, users, rooms, admin, fantasy

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(wallet.router, prefix="/wallet", tags=["Wallet"])
api_router.include_router(matches.router, prefix="/matches", tags=["Matches"])
api_router.include_router(rooms.router, prefix="/rooms", tags=["Match Rooms"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])
api_router.include_router(fantasy.router, prefix="/fantasy", tags=["Fantasy Football"])
