"""
Socket.IO Manager
Handles real-time chat and presence
"""
import socketio
from app.core.config import settings

# Create Socket.IO server
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=settings.CORS_ORIGINS,
    logger=settings.DEBUG,
    engineio_logger=settings.DEBUG
)

@sio.event
async def connect(sid, environ, auth):
    """Handle client connection"""
    print(f"Client connected: {sid}")
    await sio.emit('connected', {'sid': sid}, room=sid)

@sio.event
async def disconnect(sid):
    """Handle client disconnection"""
    print(f"Client disconnected: {sid}")

@sio.event
async def join_room(sid, data):
    """Join a match room"""
    room = f"match_{data['match_id']}"
    await sio.enter_room(sid, room)
    await sio.emit('room_joined', {
        'match_id': data['match_id'],
        'room': room
    }, room=sid)
    print(f"Client {sid} joined room {room}")

@sio.event
async def leave_room(sid, data):
    """Leave a match room"""
    room = f"match_{data['match_id']}"
    await sio.leave_room(sid, room)
    await sio.emit('room_left', {
        'match_id': data['match_id']
    }, room=sid)
    print(f"Client {sid} left room {room}")

@sio.event
async def send_message(sid, data):
    """Send chat message to room"""
    room = f"match_{data['match_id']}"
    message = {
        'user_id': data.get('user_id'),
        'username': data.get('username'),
        'content': data.get('content'),
        'type': data.get('type', 'text'),
        'timestamp': data.get('timestamp')
    }
    await sio.emit('new_message', message, room=room, skip_sid=sid)
    print(f"Message sent to room {room}")

@sio.event
async def send_reaction(sid, data):
    """Send camera reaction to room"""
    room = f"match_{data['match_id']}"
    reaction = {
        'user_id': data.get('user_id'),
        'username': data.get('username'),
        'media_url': data.get('media_url'),
        'type': 'reaction',
        'timestamp': data.get('timestamp')
    }
    await sio.emit('new_reaction', reaction, room=room, skip_sid=sid)
    print(f"Reaction sent to room {room}")
