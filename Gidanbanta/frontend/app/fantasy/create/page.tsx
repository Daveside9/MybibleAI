'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { useRouter } from 'next/navigation';
import { api } from '@/lib/api';

interface Player {
  id: number;
  name: string;
  position: 'GK' | 'DEF' | 'MID' | 'FWD';
  team: string;
  cost: number;
  points: number;
}

const FORMATIONS = ['4-3-3', '4-4-2', '3-5-2', '3-4-3'];
const INITIAL_BUDGET = 200;

export default function CreateTeamPage() {
  const { user } = useAuth();
  const router = useRouter();
  const [teamName, setTeamName] = useState('');
  const [formation, setFormation] = useState('4-3-3');
  const [players, setPlayers] = useState<Player[]>([]);
  const [selectedPlayers, setSelectedPlayers] = useState<Player[]>([]);
  const [captainId, setCaptainId] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [filterPosition, setFilterPosition] = useState<string>('');

  useEffect(() => {
    if (!user) {
      router.push('/login');
      return;
    }
    fetchPlayers();
  }, [user, router]);

  const fetchPlayers = async () => {
    try {
      setLoading(true);
      const response = await api.getFantasyPlayers();
      if (response.data) {
        setPlayers(response.data as Player[]);
      } else if (response.error) {
        setError(response.error);
      }
    } catch (err) {
      setError('Failed to load players');
    } finally {
      setLoading(false);
    }
  };

  const budgetUsed = selectedPlayers.reduce((sum, p) => sum + p.cost, 0);
  const budgetRemaining = INITIAL_BUDGET - budgetUsed;

  const togglePlayer = (player: Player) => {
    if (selectedPlayers.find(p => p.id === player.id)) {
      setSelectedPlayers(selectedPlayers.filter(p => p.id !== player.id));
      if (captainId === player.id) setCaptainId(null);
    } else {
      if (selectedPlayers.length < 11) {
        setSelectedPlayers([...selectedPlayers, player]);
      }
    }
  };

  const handleCreateTeam = async () => {
    if (!teamName.trim()) {
      setError('Please enter a team name');
      return;
    }
    if (selectedPlayers.length !== 11) {
      setError('Please select exactly 11 players');
      return;
    }
    if (!captainId) {
      setError('Please select a captain');
      return;
    }

    try {
      setCreating(true);
      setError(null);
      
      // Debug: Check authentication state
      const token = localStorage.getItem('access_token');
      const refreshToken = localStorage.getItem('refresh_token');
      console.log('Current auth token exists:', !!token);
      console.log('Current refresh token exists:', !!refreshToken);
      console.log('Current user:', user);
      
      if (token) {
        // Try to decode token to check expiry (basic check)
        try {
          const tokenParts = token.split('.');
          if (tokenParts.length === 3) {
            const payload = JSON.parse(atob(tokenParts[1]));
            const now = Math.floor(Date.now() / 1000);
            console.log('Token expires at:', new Date(payload.exp * 1000));
            console.log('Token is expired:', payload.exp < now);
          }
        } catch (e) {
          console.log('Could not decode token for debugging');
        }
      }
      
      console.log('Creating team with:', {
        name: teamName,
        formation,
        player_ids: selectedPlayers.map(p => p.id),
        captain_player_id: captainId,
      });
      
      const response = await api.createFantasyTeam({
        name: teamName,
        formation,
        player_ids: selectedPlayers.map(p => p.id),
        captain_player_id: captainId,
      });

      console.log('Create team response:', response);

      if (response.error) {
        console.error('Error creating team:', response.error);
        
        // Handle authentication errors specifically
        if (response.error.includes('Could not validate credentials') || 
            response.error.includes('401') || 
            response.error.includes('Unauthorized')) {
          setError('Your session has expired. Please log in again.');
          // Clear tokens and redirect to login
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          setTimeout(() => {
            router.push('/login');
          }, 2000);
        } else {
          setError(response.error);
        }
      } else {
        console.log('Team created successfully, redirecting...');
        router.push('/fantasy');
      }
    } catch (err) {
      console.error('Exception creating team:', err);
      setError('Failed to create team: ' + (err instanceof Error ? err.message : 'Unknown error'));
    } finally {
      setCreating(false);
    }
  };

  const filteredPlayers = filterPosition
    ? players.filter(p => p.position === filterPosition)
    : players;

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-white text-xl">Loading players...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen relative">
      <div 
        className="fixed inset-0 z-0"
        style={{
          backgroundImage: "url('https://wallpaperaccess.com/full/5183440.jpg')",
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          backgroundRepeat: 'no-repeat'
        }}
      >
        <div className="absolute inset-0 bg-black/70"></div>
      </div>
      
      <div className="relative z-10 p-6">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-blue-400 mb-6">Create Fantasy Team</h1>

        {error && (
          <div className="bg-red-900/20 border border-red-500 rounded-lg p-4 mb-6">
            <p className="text-red-500">{error}</p>
          </div>
        )}

        {/* Team Info */}
        <div className="rounded-lg p-6 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-400 mb-2">Team Name</label>
              <input
                type="text"
                value={teamName}
                onChange={(e) => setTeamName(e.target.value)}
                className="w-full bg-white/10 backdrop-blur text-white rounded px-4 py-2"
                placeholder="Enter team name"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-400 mb-2">Formation</label>
              <select
                value={formation}
                onChange={(e) => setFormation(e.target.value)}
                className="w-full bg-white/10 backdrop-blur text-white rounded px-4 py-2"
              >
                {FORMATIONS.map(f => (
                  <option key={f} value={f} className="bg-black text-white">{f}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-400 mb-2">Budget</label>
              <div className="text-white text-lg">
                {budgetRemaining.toFixed(1)} / {INITIAL_BUDGET} coins
              </div>
            </div>
          </div>
        </div>

        {/* Selected Players */}
        <div className="rounded-lg p-6 mb-6">
          <h2 className="text-xl font-bold text-blue-400 mb-4">
            Selected Players ({selectedPlayers.length}/11)
          </h2>
          {selectedPlayers.length === 0 ? (
            <p className="text-gray-400">No players selected yet</p>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
              {selectedPlayers.map(player => (
                <div key={player.id} className="bg-white/10 backdrop-blur rounded p-3 flex items-center justify-between">
                  <div>
                    <div className="text-white font-semibold">{player.name}</div>
                    <div className="text-sm text-gray-400">{player.position} - {player.team}</div>
                  </div>
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => setCaptainId(player.id)}
                      className={`px-2 py-1 rounded text-xs ${
                        captainId === player.id
                          ? 'bg-yellow-500 text-black'
                          : 'bg-white/20 backdrop-blur text-white'
                      }`}
                    >
                      C
                    </button>
                    <button
                      onClick={() => togglePlayer(player)}
                      className="text-red-500 hover:text-red-400"
                    >
                      ✕
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Available Players */}
        <div className="rounded-lg p-6 mb-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold text-blue-400">Available Players</h2>
            <select
              value={filterPosition}
              onChange={(e) => setFilterPosition(e.target.value)}
              className="bg-white/10 backdrop-blur text-white rounded px-4 py-2"
            >
              <option value="" className="bg-black text-white">All Positions</option>
              <option value="GK" className="bg-black text-white">Goalkeepers</option>
              <option value="DEF" className="bg-black text-white">Defenders</option>
              <option value="MID" className="bg-black text-white">Midfielders</option>
              <option value="FWD" className="bg-black text-white">Forwards</option>
            </select>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {filteredPlayers.map(player => {
              const isSelected = selectedPlayers.find(p => p.id === player.id);
              const canAfford = budgetRemaining >= player.cost || isSelected;
              
              return (
                <button
                  key={player.id}
                  onClick={() => togglePlayer(player)}
                  disabled={!canAfford && !isSelected}
                  className={`p-2 rounded text-left transition shadow-lg shadow-blue-500/30 ${
                    isSelected
                      ? 'text-green-400 border border-green-400/50'
                      : canAfford
                      ? 'text-white hover:shadow-blue-500/50'
                      : 'text-gray-500 cursor-not-allowed opacity-50'
                  }`}
                >
                  <div className="text-sm font-semibold">{player.name}</div>
                  <div className="text-xs opacity-80">{player.position} - {player.team}</div>
                  <div className="text-xs mt-1">Cost: {player.cost} | Points: {player.points}</div>
                </button>
              );
            })}
          </div>
        </div>

        {/* Actions */}
        <div className="space-y-4">
          {/* Validation Messages */}
          <div className="rounded-lg p-4">
            <h3 className="text-blue-400 font-semibold mb-2">Checklist:</h3>
            <div className="space-y-1 text-sm">
              <div className={teamName.trim() ? 'text-green-500' : 'text-gray-400'}>
                {teamName.trim() ? '✓' : '○'} Team name entered
              </div>
              <div className={selectedPlayers.length === 11 ? 'text-green-500' : 'text-gray-400'}>
                {selectedPlayers.length === 11 ? '✓' : '○'} 11 players selected ({selectedPlayers.length}/11)
              </div>
              <div className={captainId ? 'text-green-500' : 'text-gray-400'}>
                {captainId ? '✓' : '○'} Captain selected
              </div>
            </div>
          </div>

          <div className="flex gap-4">
            <button
              onClick={handleCreateTeam}
              disabled={creating || selectedPlayers.length !== 11 || !captainId || !teamName.trim()}
              className="bg-green-600/80 backdrop-blur hover:bg-green-700/80 disabled:bg-gray-600/50 disabled:cursor-not-allowed text-white px-6 py-3 rounded-lg font-semibold"
            >
              {creating ? 'Creating...' : 'Create Team'}
            </button>
            <button
              onClick={() => router.push('/fantasy')}
              className="bg-white/10 backdrop-blur hover:bg-white/20 text-white px-6 py-3 rounded-lg font-semibold"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
      </div>
    </div>
  );
}
