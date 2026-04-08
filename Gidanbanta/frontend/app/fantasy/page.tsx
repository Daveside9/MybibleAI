'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { useRouter } from 'next/navigation';
import { api } from '@/lib/api';
import { Home } from 'lucide-react';

interface Player {
  id: number;
  name: string;
  position: 'GK' | 'DEF' | 'MID' | 'FWD';
  team: string;
  cost: number;
  points: number;
  goals: number;
  assists: number;
  clean_sheets: number;
}

interface TeamPlayer {
  id: number;
  player: Player;
  is_captain: boolean;
  position_in_formation: number;
}

interface FantasyTeam {
  id: number;
  name: string;
  formation: string;
  team_players: TeamPlayer[];
  total_points: number;
  budget_remaining: number;
  captain_player_id: number | null;
}

export default function FantasyPage() {
  const { user } = useAuth();
  const router = useRouter();
  const [team, setTeam] = useState<FantasyTeam | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!user) {
      router.push('/login');
      return;
    }

    fetchTeam();
  }, [user, router]);

  const fetchTeam = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await api.getFantasyTeam();
      
      if (response.error) {
        // User doesn't have a team yet (404) or other error
        if (response.error.includes('not found')) {
          setTeam(null);
        } else {
          setError(response.error);
        }
      } else if (response.data) {
        setTeam(response.data as FantasyTeam);
      }
    } catch (err: any) {
      setError('Failed to load fantasy team');
      console.error('Error fetching team:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-white text-xl">Loading...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen relative">
        <div 
          className="fixed inset-0 z-0"
          style={{
            backgroundImage: "url('https://wallpaperaccess.com/full/780050.jpg')",
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            backgroundRepeat: 'no-repeat'
          }}
        >
          <div className="absolute inset-0 bg-black/70"></div>
        </div>
        
        <div className="relative z-10 p-6">
          <div className="max-w-4xl mx-auto">
            <div className="border border-red-500 rounded-lg p-8 text-center">
              <h1 className="text-2xl font-bold text-blue-400 mb-4 shadow-lg shadow-black/50">Error</h1>
              <p className="text-gray-300 mb-6 shadow-lg shadow-black/50">{error}</p>
              <button 
                onClick={fetchTeam}
                className="bg-red-600 hover:bg-red-700 text-white px-6 py-3 rounded-lg font-semibold shadow-lg shadow-black/50"
              >
                Try Again
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!team) {
    return (
      <div className="min-h-screen relative">
        <div 
          className="fixed inset-0 z-0"
          style={{
            backgroundImage: "url('https://wallpaperaccess.com/full/780050.jpg')",
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            backgroundRepeat: 'no-repeat'
          }}
        >
          <div className="absolute inset-0 bg-black/70"></div>
        </div>
        
        <div className="relative z-10 p-6">
          <div className="max-w-4xl mx-auto">
            <div className="p-8 text-center">
              <h1 className="text-3xl font-bold text-blue-400 mb-4 shadow-lg shadow-black/50">Fantasy Football</h1>
              <p className="text-gray-400 mb-6 shadow-lg shadow-black/50">You haven't created a fantasy team yet.</p>
              <button 
                onClick={() => router.push('/fantasy/create')}
                className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg font-semibold shadow-lg shadow-black/50"
              >
                Create Your Team
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen relative">
      <div 
        className="fixed inset-0 z-0"
        style={{
          backgroundImage: "url('https://wallpaperaccess.com/full/780050.jpg')",
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          backgroundRepeat: 'no-repeat'
        }}
      >
        <div className="absolute inset-0 bg-black/70"></div>
      </div>
      
      <div className="relative z-10 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Home Button */}
        <button
          onClick={() => router.push('/dashboard')}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors mb-4"
        >
          <Home className="w-4 h-4" />
          <span>Home</span>
        </button>

        {/* Header */}
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-blue-400 mb-2 shadow-lg shadow-black/50">Fantasy Football</h1>
          <div className="flex items-center gap-4 text-gray-400">
            <span className="shadow-lg shadow-black/50">Budget Remaining: {team.budget_remaining.toFixed(1)} coins</span>
            <span className="shadow-lg shadow-black/50">•</span>
            <span className="shadow-lg shadow-black/50">Total Points: {team.total_points}</span>
          </div>
        </div>

        {/* Team Overview */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
          <div className="rounded-lg p-6">
            <h3 className="text-lg font-semibold text-blue-400 mb-2 shadow-lg shadow-black/50">Team Name</h3>
            <p className="text-gray-400 shadow-lg shadow-black/50">{team.name}</p>
          </div>
          <div className="rounded-lg p-6">
            <h3 className="text-lg font-semibold text-blue-400 mb-2 shadow-lg shadow-black/50">Formation</h3>
            <p className="text-gray-400 shadow-lg shadow-black/50">{team.formation}</p>
          </div>
          <div className="rounded-lg p-6">
            <h3 className="text-lg font-semibold text-blue-400 mb-2 shadow-lg shadow-black/50">Players</h3>
            <p className="text-gray-400 shadow-lg shadow-black/50">{team.team_players.length} / 11</p>
          </div>
        </div>

        {/* Pitch View */}
        <div className="rounded-lg p-8 mb-6">
          <div className="text-center text-white mb-4">
            <h2 className="text-2xl font-bold text-blue-400 shadow-lg shadow-black/50">Your Squad</h2>
          </div>
          
          {team.team_players.length === 0 ? (
            <div className="text-center text-white py-12">
              <p className="text-xl mb-4 shadow-lg shadow-black/50">No players selected yet</p>
              <button 
                onClick={() => router.push('/fantasy/create')}
                className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg font-semibold shadow-lg shadow-black/50"
              >
                Select Players
              </button>
            </div>
          ) : (
            <div className="space-y-6">
              {/* Player List */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {team.team_players.map((teamPlayer) => (
                  <div 
                    key={teamPlayer.id}
                    className="rounded-lg p-4"
                  >
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-white font-semibold shadow-lg shadow-blue-500/50">{teamPlayer.player.name}</span>
                      {teamPlayer.is_captain && (
                        <span className="bg-yellow-500 text-black text-xs px-2 py-1 rounded font-bold shadow-lg shadow-blue-500/50">C</span>
                      )}
                    </div>
                    <div className="text-sm text-gray-300 space-y-1">
                      <div className="flex justify-between">
                        <span className="shadow-lg shadow-blue-500/50">{teamPlayer.player.position}</span>
                        <span className="shadow-lg shadow-blue-500/50">{teamPlayer.player.team}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="shadow-lg shadow-blue-500/50">Cost: {teamPlayer.player.cost} coins</span>
                        <span className="font-semibold shadow-lg shadow-blue-500/50">{teamPlayer.player.points} pts</span>
                      </div>
                      <div className="text-xs text-gray-400 shadow-lg shadow-blue-500/50">
                        G: {teamPlayer.player.goals} | A: {teamPlayer.player.assists} | CS: {teamPlayer.player.clean_sheets}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Actions */}
        <div className="flex gap-4">
          <button 
            onClick={() => router.push('/fantasy/edit')}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-semibold shadow-lg shadow-black/50"
          >
            Edit Team
          </button>
          <button 
            onClick={() => router.push('/fantasy/leaderboard')}
            className="bg-gray-700 hover:bg-gray-600 text-white px-6 py-3 rounded-lg font-semibold shadow-lg shadow-black/50"
          >
            View Leaderboard
          </button>
          <button 
            onClick={async () => {
              if (team.total_points > 0) {
                alert('Cannot delete team after the game has started!');
                return;
              }
              
              if (confirm('Are you sure you want to delete your fantasy team? This action cannot be undone.')) {
                try {
                  const response = await api.deleteFantasyTeam();
                  if (response.error) {
                    alert('Failed to delete team: ' + response.error);
                  } else {
                    alert('Team deleted successfully!');
                    setTeam(null);
                  }
                } catch (err) {
                  alert('Failed to delete team');
                  console.error(err);
                }
              }
            }}
            disabled={team.total_points > 0}
            className={`px-6 py-3 rounded-lg font-semibold transition-all shadow-lg shadow-black/50 ${
              team.total_points > 0
                ? 'bg-gray-600 text-gray-400 cursor-not-allowed'
                : 'bg-red-600 hover:bg-red-700 text-white'
            }`}
            title={team.total_points > 0 ? 'Cannot delete team after game has started' : 'Delete team'}
          >
            Delete Team
          </button>
        </div>
      </div>
      </div>
    </div>
  );
}
