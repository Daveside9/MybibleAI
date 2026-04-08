/**
 * Socket.IO Client
 * Handles real-time communication
 */
import { io, Socket } from 'socket.io-client';

const SOCKET_URL = process.env.NEXT_PUBLIC_SOCKET_URL || 'http://localhost:4000';

class SocketClient {
  private socket: Socket | null = null;

  connect() {
    if (this.socket?.connected) {
      return this.socket;
    }

    this.socket = io(SOCKET_URL, {
      transports: ['websocket', 'polling'],
      autoConnect: true,
      timeout: 5000, // 5 second timeout
      reconnection: true,
      reconnectionAttempts: 3,
      reconnectionDelay: 1000,
    });

    this.socket.on('connect', () => {
      console.log('Socket connected:', this.socket?.id);
    });

    this.socket.on('disconnect', () => {
      console.log('Socket disconnected');
    });

    this.socket.on('connect_error', (error) => {
      console.error('Socket connection error:', error);
    });

    return this.socket;
  }

  disconnect() {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    }
  }

  joinRoom(matchId: number, userId: number, username: string) {
    if (!this.socket) return;
    
    this.socket.emit('join_room', {
      match_id: matchId,
      user_id: userId,
      username: username,
    });
  }

  leaveRoom(matchId: number) {
    if (!this.socket) return;
    
    this.socket.emit('leave_room', {
      match_id: matchId,
    });
  }

  sendMessage(matchId: number, userId: number, username: string, content: string) {
    if (!this.socket) return;
    
    this.socket.emit('send_message', {
      match_id: matchId,
      user_id: userId,
      username: username,
      content: content,
      type: 'text',
      timestamp: new Date().toISOString(),
    });
  }

  sendReaction(matchId: number, userId: number, username: string, mediaUrl: string) {
    if (!this.socket) return;
    
    this.socket.emit('send_reaction', {
      match_id: matchId,
      user_id: userId,
      username: username,
      media_url: mediaUrl,
      type: 'reaction',
      timestamp: new Date().toISOString(),
    });
  }

  onMessage(callback: (message: any) => void) {
    if (!this.socket) return;
    this.socket.on('new_message', callback);
  }

  onReaction(callback: (reaction: any) => void) {
    if (!this.socket) return;
    this.socket.on('new_reaction', callback);
  }

  onRoomJoined(callback: (data: any) => void) {
    if (!this.socket) return;
    this.socket.on('room_joined', callback);
  }

  offMessage() {
    if (!this.socket) return;
    this.socket.off('new_message');
  }

  offReaction() {
    if (!this.socket) return;
    this.socket.off('new_reaction');
  }

  getSocket() {
    return this.socket;
  }
}

export const socketClient = new SocketClient();
