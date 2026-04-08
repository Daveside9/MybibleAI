'use client';

import { useEffect, useState, useRef } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import { api } from '@/lib/api';
import { socketClient } from '@/lib/socket';
import PageNavigation from '@/components/PageNavigation';
import VideoPlayer from '@/components/VideoPlayer';

interface Match {
  id: number;
  title: string;
  home_team: string;
  away_team: string;
  home_score: number;
  away_score: number;
  status: string;
  scheduled_at: string;
  stream_url?: string;
}

interface ChatMessage {
  id: string;
  user_id: number;
  username: string;
  content: string;
  type: 'text' | 'reaction' | 'emoji';
  timestamp: string;
  media_url?: string;
}

export default function MatchRoomPage() {
  const params = useParams();
  const router = useRouter();
  const { user, loading: authLoading } = useAuth();
  const matchId = parseInt(params.id as string);

  const [match, setMatch] = useState<Match | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(true);

  const [hasChatAccess, setHasChatAccess] = useState(false);
  const [freeMessagesLeft, setFreeMessagesLeft] = useState(3);
  const [showUnlockModal, setShowUnlockModal] = useState(false);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);


  useEffect(() => {
    if (!authLoading && !user) {
      router.push('/login');
      return;
    }

    // Validate match ID - if it's clearly invalid, redirect immediately
    if (isNaN(matchId) || matchId <= 0) {
      console.error(`❌ Invalid match ID: ${matchId}`);
      router.push('/dashboard');
      return;
    }

    if (user) {
      // Load match data immediately
      loadMatch();
      
      // Connect socket after a short delay to not block initial load
      const socketTimer = setTimeout(() => {
        connectSocket();
      }, 100);

      return () => {
        clearTimeout(socketTimer);
        socketClient.leaveRoom(matchId);
        socketClient.disconnect();
      };
    }
  }, [user, authLoading, matchId]);

  const loadMatch = async () => {
    const startTime = performance.now();
    console.log(`🚀 Starting to load match data for ID: ${matchId}...`);
    
    try {
      // Load match data first (priority)
      const matchStart = performance.now();
      const matchResponse = await api.getMatch(matchId);
      const matchEnd = performance.now();
      console.log(`📊 Match API call took: ${(matchEnd - matchStart).toFixed(2)}ms`);
      
      if (matchResponse.data) {
        setMatch(matchResponse.data as Match);
        setLoading(false); // Show page as soon as match data is loaded
        console.log('✅ Match data loaded, page visible');
      } else if (matchResponse.error) {
        console.error(`❌ Failed to load match ID ${matchId}:`, matchResponse.error);
        setLoading(false);
        
        // If match not found, redirect to dashboard immediately
        if (matchResponse.error.includes('Not Found') || matchResponse.error.includes('404')) {
          console.log(`🔄 Match ID ${matchId} not found, redirecting to dashboard...`);
          router.push('/dashboard');
        }
        return; // Don't try to load room data if match doesn't exist
      }

      // Load room data in background
      const roomStart = performance.now();
      const roomResponse = await api.joinRoom(matchId);
      const roomEnd = performance.now();
      console.log(`📊 Room API call took: ${(roomEnd - roomStart).toFixed(2)}ms`);
      
      if (roomResponse.data) {
        const roomData = roomResponse.data as any;
        setHasChatAccess(roomData.has_chat_access);
        setFreeMessagesLeft(roomData.free_messages_left);
        console.log('✅ Room data loaded');
      } else if (roomResponse.error) {
        console.error('Failed to join room:', roomResponse.error);
      }
      
      const totalTime = performance.now() - startTime;
      console.log(`🏁 Total loading time: ${totalTime.toFixed(2)}ms`);
    } catch (error) {
      console.error('Error loading match data:', error);
      setLoading(false);
    }
  };

  const connectSocket = () => {
    if (!user) return;

    const socketStart = performance.now();
    console.log('🔌 Connecting to socket...');

    try {
      socketClient.connect();
      socketClient.joinRoom(matchId, user.id, user.username);

      socketClient.onRoomJoined((data) => {
        const socketEnd = performance.now();
        console.log(`✅ Socket connected and joined room in ${(socketEnd - socketStart).toFixed(2)}ms`);
        console.log('Room data:', data);
      });

      socketClient.onMessage((message) => {
        setMessages((prev) => [...prev, {
          ...message,
          id: `${message.user_id}-${Date.now()}`,
        }]);
      });

      socketClient.onReaction((reaction) => {
        setMessages((prev) => [...prev, {
          ...reaction,
          id: `${reaction.user_id}-${Date.now()}`,
        }]);
      });
    } catch (error) {
      console.error('Socket connection failed:', error);
      // Continue without socket - the page should still work
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || !user) return;

    // Check if user has chat access
    if (!hasChatAccess && freeMessagesLeft <= 0) {
      setShowUnlockModal(true);
      return;
    }

    // Track message on backend
    const response = await api.sendMessage(matchId);
    if (response.error) {
      alert(response.error);
      return;
    }

    // Send message via socket
    socketClient.sendMessage(matchId, user.id, user.username, inputMessage);
    
    // Add to local messages
    setMessages((prev) => [...prev, {
      id: `${user.id}-${Date.now()}`,
      user_id: user.id,
      username: user.username,
      content: inputMessage,
      type: 'text',
      timestamp: new Date().toISOString(),
    }]);

    // Update free messages count
    if (response.data) {
      const data = response.data as any;
      setFreeMessagesLeft(data.free_messages_left);
      setHasChatAccess(data.has_chat_access);
    }

    setInputMessage('');
  };

  const handleUnlockChat = async () => {
    try {
      const response = await api.unlockChat(matchId);
      
      if (response.error) {
        // Handle specific error cases
        if (response.error.includes('18+') || response.error.includes('KYC')) {
          alert('Chat unlock requires age verification (18+) and KYC completion. Please contact support or use the admin account for testing.');
        } else {
          alert(response.error);
        }
        return;
      }

      const data = response.data as any;
      setHasChatAccess(true);
      setShowUnlockModal(false);
      alert(`Chat unlocked! New balance: ₦${data.new_balance}`);
    } catch (error) {
      console.error('Failed to unlock chat:', error);
      alert('Failed to unlock chat. Please try again or contact support.');
    }
  };

  if (authLoading || loading) {
    return (
      <div className="min-h-screen bg-navy flex items-center justify-center">
        <div className="text-text-primary text-xl">Loading match...</div>
      </div>
    );
  }

  if (!match) {
    return (
      <div className="min-h-screen bg-navy flex items-center justify-center">
        <div className="text-center max-w-md mx-auto p-6">
          <div className="text-6xl mb-4">⚽</div>
          <div className="text-text-primary text-xl mb-4">Match Not Available</div>
          <div className="text-text-muted text-sm mb-6">
            Match ID {matchId} could not be found. This match may have been removed or the link is outdated.
            <br />
            <br />
            You'll be redirected to the dashboard to see available matches.
          </div>
          <button
            onClick={() => router.push('/dashboard')}
            className="px-6 py-3 bg-primary hover:bg-primary-600 text-white rounded-lg transition-all"
          >
            Go to Dashboard
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-navy flex flex-col">
      {/* Header */}
      <header className="bg-navy-100 border-b border-navy-200 px-4 py-3">
        <PageNavigation className="mb-2" />
        <div className="flex items-center justify-between">
          <button
            onClick={() => router.push('/dashboard')}
            className="text-text-muted hover:text-text-primary"
          >
            ← Back
          </button>
          <div className="text-center flex-1">
            <h1 className="text-lg font-semibold text-text-primary">
              {match.title}
            </h1>
            <div className="text-sm text-text-muted">
              {match.home_team} vs {match.away_team}
            </div>
          </div>
          <div className={`px-3 py-1 rounded-full text-xs font-semibold ${
            match.status === 'live' 
              ? 'bg-danger text-white' 
              : 'bg-navy text-text-muted'
          }`}>
            {match.status === 'live' ? '🔴 LIVE' : match.status}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex-1 flex flex-col lg:flex-row overflow-hidden bg-gray-900">
        {/* Video Player Section */}
        <div className="lg:w-2/3 bg-gray-900 flex flex-col">
          {/* Video Player */}
          <div className="p-4 flex-1 flex items-center justify-center">
            <VideoPlayer
              streamUrl={match.stream_url}
              isLive={match.status === 'live'}
              title={`${match.home_team} vs ${match.away_team}`}
            />
          </div>
          
          {/* Match Info */}
          <div className="p-4 bg-gray-800 border-t border-gray-700">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-6">
                <div className="text-center">
                  <div className="text-white font-semibold">{match.home_team}</div>
                  <div className="text-2xl font-bold text-blue-400">{match.home_score || 0}</div>
                </div>
                <div className="text-gray-400 text-sm">VS</div>
                <div className="text-center">
                  <div className="text-white font-semibold">{match.away_team}</div>
                  <div className="text-2xl font-bold text-blue-400">{match.away_score || 0}</div>
                </div>
              </div>
              
              <div className="text-right">
                <div className={`px-3 py-1 rounded-full text-xs font-semibold mb-2 ${
                  match.status === 'live' 
                    ? 'bg-red-600 text-white' 
                    : match.status === 'finished'
                    ? 'bg-gray-600 text-gray-300'
                    : 'bg-blue-600 text-white'
                }`}>
                  {match.status === 'live' ? '🔴 LIVE' : match.status.toUpperCase()}
                </div>
                <div className="text-xs text-gray-400">
                  {new Date(match.scheduled_at).toLocaleString()}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Chat Sidebar */}
        <div className="lg:w-1/3 bg-navy-100 flex flex-col border-l border-navy-200">
          {/* Chat Header */}
          <div className="px-4 py-3 border-b border-navy-200">
            <h2 className="font-semibold text-text-primary">Live Chat</h2>
            {!hasChatAccess && (
              <div className="text-xs text-text-muted mt-1">
                {freeMessagesLeft} free messages left
              </div>
            )}
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {messages.length === 0 ? (
              <div className="text-center text-text-muted text-sm py-8">
                No messages yet. Be the first to chat!
              </div>
            ) : (
              messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.user_id === user?.id ? 'justify-end' : 'justify-start'}`}
                >
                  <div className={`max-w-[80%] ${
                    message.user_id === user?.id
                      ? 'bg-primary text-white'
                      : 'bg-navy'
                  } rounded-lg px-3 py-2`}>
                    <div className="text-xs opacity-75 mb-1">
                      {message.username}
                    </div>
                    {message.type === 'reaction' ? (
                      <div className="text-sm">📹 Camera reaction</div>
                    ) : (
                      <div className="text-sm">{message.content}</div>
                    )}
                  </div>
                </div>
              ))
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Message Input */}
          <div className="p-4 border-t border-navy-200">
            <div className="flex gap-2">
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
                placeholder={
                  hasChatAccess 
                    ? "Type a message..." 
                    : `${freeMessagesLeft} free messages left`
                }
                className="flex-1 px-4 py-2 bg-navy border border-navy-200 rounded-lg text-text-primary focus:outline-none focus:border-primary"
              />
              <button
                onClick={handleSendMessage}
                disabled={!inputMessage.trim()}
                className="px-4 py-2 bg-primary hover:bg-primary-600 text-white rounded-lg disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Send
              </button>
            </div>
            {!hasChatAccess && freeMessagesLeft === 0 && (
              <button
                onClick={() => setShowUnlockModal(true)}
                className="w-full mt-2 px-4 py-2 bg-cyan hover:bg-cyan/80 text-navy font-semibold rounded-lg"
              >
                Unlock Chat - ₦100
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Unlock Modal */}
      {showUnlockModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-navy-100 rounded-card p-6 max-w-md w-full">
            <h2 className="text-2xl font-heading font-bold text-text-primary mb-4">
              Unlock Chat
            </h2>
            <p className="text-text-muted mb-6">
              Unlock unlimited chat for this match for only ₦100. 
              Valid until the match ends.
            </p>
            <div className="flex gap-3">
              <button
                onClick={() => setShowUnlockModal(false)}
                className="flex-1 px-4 py-3 bg-navy hover:bg-navy-200 text-text-primary rounded-lg"
              >
                Cancel
              </button>
              <button
                onClick={handleUnlockChat}
                className="flex-1 px-4 py-3 bg-primary hover:bg-primary-600 text-white font-semibold rounded-lg"
              >
                Pay ₦100
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
