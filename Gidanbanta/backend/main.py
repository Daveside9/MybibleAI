"""
MatchHang FastAPI Application
Main entry point for the API server
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import socketio
from contextlib import asynccontextmanager
from slowapi.errors import RateLimitExceeded

from app.core.config import settings
from app.core.database import engine, Base
from app.api.v1.router import api_router
from app.sockets.manager import sio
from app.middleware.rate_limit import limiter, rate_limit_exceeded_handler

# Create tables on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting MatchHang API...")
    # Create database tables
    # Base.metadata.create_all(bind=engine)
    yield
    # Shutdown
    print("👋 Shutting down MatchHang API...")

# Initialize FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    description="Live match streaming + social viewing rooms",
    version=settings.API_VERSION,
    lifespan=lifespan
)

# Add rate limiter state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Socket.IO
socket_app = socketio.ASGIApp(
    sio,
    other_asgi_app=app,
    socketio_path="/socket.io"
)

# Include API routes
app.include_router(api_router, prefix=f"/{settings.API_VERSION}")

# Health check
@app.get("/health")
async def health_check():
    return JSONResponse({
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.API_VERSION
    })

@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.APP_NAME} API",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:socket_app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
