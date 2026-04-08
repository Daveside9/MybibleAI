'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { useRouter } from 'next/navigation';
import { api } from '@/lib/api';

interface LeaderboardEntry {
  rank: number;
  team_name: string;
  username: string;
  total_points: number;
  formation: string;
}

export default function LeaderboardPage() {
  const { user } = useAuth();
  const router = useRouter();
  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!user) {
      router.push('/login');
      return;
    }
    fetchLeaderboard();
  }, [user, router]);

  const fetchLeaderboard = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await api.getFantasyLeaderboard(50);
      
      if (response.error) {
        setError(response.error);
      } else if (response.data) {
        setLeaderboard(response.data as LeaderboardEntry[]);
      }
    } catch (err) {
      setError('Failed to load leaderboard');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-white text-xl">Loading leaderboard...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 p-6">
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-3xl font-bold text-white">Fantasy Leaderboard</h1>
          <button
            onClick={() => router.push('/fantasy')}
            className="bg-gray-700 hover:bg-gray-600 text-white px-4 py-2 rounded-lg"
          >
            Back to My Team
          </button>
        </div>

        {error && (
          <div className="bg-red-900/20 border border-red-500 rounded-lg p-4 mb-6">
            <p className="text-red-500">{error}</p>
          </div>
        )}

        {leaderboard.length === 0 ? (
          <div className="bg-gray-800 rounded-lg p-8 text-center">
            <p className="text-gray-400 text-lg">No teams on the leaderboard yet.</p>
            <p className="text-gray-500 mt-2">Be the first to create a team!</p>
          </div>
        ) : (
          <div className="bg-gray-800 rounded-lg overflow-hidden">
            <table className="w-full">
              <thead className="bg-gray-700">
                <tr>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-300">Rank</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-300">Team Name</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-300">Manager</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-300">Formation</th>
                  <th className="px-6 py-4 text-right text-sm font-semibold text-gray-300">Points</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-700">
                {leaderboard.map((entry) => (
                  <tr 
                    key={entry.rank}
                    className={`hover:bg-gray-750 transition ${
                      entry.username === user?.username ? 'bg-blue-900/20' : ''
                    }`}
                  >
                    <td className="px-6 py-4">
                      <div className="flex items-center">
                        {entry.rank <= 3 ? (
                          <span className="text-2xl">
                            {entry.rank === 1 ? '🥇' : entry.rank === 2 ? '🥈' : '🥉'}
                          </span>
                        ) : (
                          <span className="text-gray-400 font-semibold">{entry.rank}</span>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="text-white font-semibold">{entry.team_name}</div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="text-gray-300">
                        {entry.username}
                        {entry.username === user?.username && (
                          <span className="ml-2 text-xs bg-blue-600 px-2 py-1 rounded">You</span>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="text-gray-400">{entry.formation}</div>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <div className="text-green-500 font-bold text-lg">{entry.total_points}</div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
