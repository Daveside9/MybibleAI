'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import { api } from '@/lib/api';
import PageNavigation from '@/components/PageNavigation';

interface Stats {
  users: {
    total: number;
    active: number;
    banned: number;
  };
  matches: {
    total: number;
    live: number;
  };
  wallet: {
    total_balance: number;
  };
}

interface Match {
  id: number;
  title: string;
  home_team: string;
  away_team: string;
  status: string;
  scheduled_at: string;
}

export default function AdminDashboard() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  const [stats, setStats] = useState<Stats | null>(null);
  const [matches, setMatches] = useState<Match[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreateMatch, setShowCreateMatch] = useState(false);
  const [newMatch, setNewMatch] = useState({
    title: '',
    home_team: '',
    away_team: '',
    scheduled_at: '',
  });

  useEffect(() => {
    if (!authLoading && !user) {
      router.push('/login');
    } else if (user && user.role !== 'admin' && user.role !== 'moderator') {
      router.push('/dashboard');
    } else if (user) {
      loadData();
    }
  }, [user, authLoading]);

  const loadData = async () => {
    setLoading(true);

    // Load stats
    const statsResponse = await fetch('http://localhost:4000/v1/admin/stats', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    });
    if (statsResponse.ok) {
      const data = await statsResponse.json();
      setStats(data);
    }

    // Load matches
    const matchesResponse = await fetch('http://localhost:4000/v1/admin/matches', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    });
    if (matchesResponse.ok) {
      const data = await matchesResponse.json();
      setMatches(data);
    }

    setLoading(false);
  };

  const handleCreateMatch = async () => {
    const response = await fetch('http://localhost:4000/v1/admin/matches', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      },
      body: JSON.stringify({
        ...newMatch,
        is_featured: true
      })
    });

    if (response.ok) {
      alert('Match created successfully!');
      setShowCreateMatch(false);
      setNewMatch({ title: '', home_team: '', away_team: '', scheduled_at: '' });
      loadData();
    } else {
      alert('Failed to create match');
    }
  };

  const handleUpdateStatus = async (matchId: number, status: string) => {
    const response = await fetch(`http://localhost:4000/v1/admin/matches/${matchId}/status?status=${status}`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    });

    if (response.ok) {
      alert(`Match status updated to ${status}`);
      loadData();
    } else {
      alert('Failed to update match status');
    }
  };

  if (authLoading || loading) {
    return (
      <div className="min-h-screen bg-navy flex items-center justify-center">
        <div className="text-text-primary text-xl">Loading admin dashboard...</div>
      </div>
    );
  }

  if (!user || (user.role !== 'admin' && user.role !== 'moderator')) {
    return null;
  }

  return (
    <div className="min-h-screen bg-navy">
      {/* Header */}
      <header className="bg-navy-100 border-b border-navy-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div>
            <h1 className="text-2xl font-heading font-bold text-text-primary">
              Admin Dashboard
            </h1>
            <p className="text-sm text-text-muted">Manage MatchHang platform</p>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <PageNavigation />
        {/* Stats Cards */}
        {stats && (
          <div className="grid md:grid-cols-4 gap-6 mb-8">
            <div className="bg-navy-100 rounded-card p-6">
              <div className="text-sm text-text-muted mb-2">Total Users</div>
              <div className="text-3xl font-bold text-text-primary">{stats.users.total}</div>
            </div>
            <div className="bg-navy-100 rounded-card p-6">
              <div className="text-sm text-text-muted mb-2">Active Users</div>
              <div className="text-3xl font-bold text-success">{stats.users.active}</div>
            </div>
            <div className="bg-navy-100 rounded-card p-6">
              <div className="text-sm text-text-muted mb-2">Total Matches</div>
              <div className="text-3xl font-bold text-text-primary">{stats.matches.total}</div>
            </div>
            <div className="bg-navy-100 rounded-card p-6">
              <div className="text-sm text-text-muted mb-2">Live Matches</div>
              <div className="text-3xl font-bold text-danger">{stats.matches.live}</div>
            </div>
          </div>
        )}

        {/* Matches Management */}
        <div className="bg-navy-100 rounded-card p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-heading font-bold text-text-primary">
              Matches Management
            </h2>
            <button
              onClick={() => setShowCreateMatch(true)}
              className="px-4 py-2 bg-primary hover:bg-primary-600 text-white rounded-lg font-semibold"
            >
              + Create Match
            </button>
          </div>

          {matches.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-text-muted">No matches yet. Create your first match!</p>
            </div>
          ) : (
            <div className="space-y-4">
              {matches.map((match) => (
                <div
                  key={match.id}
                  className="bg-navy rounded-lg p-4 flex items-center justify-between"
                >
                  <div>
                    <h3 className="font-semibold text-text-primary">{match.title}</h3>
                    <p className="text-sm text-text-muted">
                      {match.home_team} vs {match.away_team}
                    </p>
                    <p className="text-xs text-text-muted mt-1">
                      {new Date(match.scheduled_at).toLocaleString()}
                    </p>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                      match.status === 'live' 
                        ? 'bg-danger text-white' 
                        : match.status === 'finished'
                        ? 'bg-navy-200 text-text-muted'
                        : 'bg-primary text-white'
                    }`}>
                      {match.status}
                    </span>
                    {match.status === 'scheduled' && (
                      <button
                        onClick={() => handleUpdateStatus(match.id, 'live')}
                        className="px-3 py-1 bg-danger hover:bg-danger/80 text-white rounded-lg text-sm"
                      >
                        Start Live
                      </button>
                    )}
                    {match.status === 'live' && (
                      <button
                        onClick={() => handleUpdateStatus(match.id, 'finished')}
                        className="px-3 py-1 bg-navy-200 hover:bg-navy-300 text-text-primary rounded-lg text-sm"
                      >
                        End Match
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>

      {/* Create Match Modal */}
      {showCreateMatch && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-navy-100 rounded-card p-6 max-w-md w-full">
            <h2 className="text-2xl font-heading font-bold text-text-primary mb-4">
              Create New Match
            </h2>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-text-primary mb-2">
                  Match Title
                </label>
                <input
                  type="text"
                  value={newMatch.title}
                  onChange={(e) => setNewMatch({ ...newMatch, title: e.target.value })}
                  placeholder="e.g., Premier League - Chelsea vs Arsenal"
                  className="w-full px-4 py-3 bg-navy border border-navy-200 rounded-lg text-text-primary focus:outline-none focus:border-primary"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-text-primary mb-2">
                  Home Team
                </label>
                <input
                  type="text"
                  value={newMatch.home_team}
                  onChange={(e) => setNewMatch({ ...newMatch, home_team: e.target.value })}
                  placeholder="Chelsea"
                  className="w-full px-4 py-3 bg-navy border border-navy-200 rounded-lg text-text-primary focus:outline-none focus:border-primary"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-text-primary mb-2">
                  Away Team
                </label>
                <input
                  type="text"
                  value={newMatch.away_team}
                  onChange={(e) => setNewMatch({ ...newMatch, away_team: e.target.value })}
                  placeholder="Arsenal"
                  className="w-full px-4 py-3 bg-navy border border-navy-200 rounded-lg text-text-primary focus:outline-none focus:border-primary"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-text-primary mb-2">
                  Scheduled Time
                </label>
                <input
                  type="datetime-local"
                  value={newMatch.scheduled_at}
                  onChange={(e) => setNewMatch({ ...newMatch, scheduled_at: e.target.value })}
                  className="w-full px-4 py-3 bg-navy border border-navy-200 rounded-lg text-text-primary focus:outline-none focus:border-primary"
                />
              </div>
            </div>

            <div className="flex gap-3 mt-6">
              <button
                onClick={() => setShowCreateMatch(false)}
                className="flex-1 px-4 py-3 bg-navy hover:bg-navy-200 text-text-primary rounded-lg"
              >
                Cancel
              </button>
              <button
                onClick={handleCreateMatch}
                disabled={!newMatch.title || !newMatch.home_team || !newMatch.away_team || !newMatch.scheduled_at}
                className="flex-1 px-4 py-3 bg-primary hover:bg-primary-600 text-white font-semibold rounded-lg disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Create Match
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
