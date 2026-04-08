'use client';

import Link from 'next/link';
import { formatMatchTime } from '@/lib/timeUtils';

interface Match {
  id: number;
  home_team: string;
  away_team: string;
  home_score: number | null;
  away_score: number | null;
  status: string;
  scheduled_time: string;
  home_odds: number;
  away_odds: number;
  draw_odds: number;
  league: {
    name: string;
    country: string;
    logo?: string;
  } | null;
  home_team_logo?: string;
  away_team_logo?: string;
}

interface MatchTableProps {
  matches: Match[];
  selectedDate: string;
  onBetClick?: (match: Match, betType: 'home' | 'draw' | 'away') => void;
  loading?: boolean;
}

export default function MatchTable({ 
  matches, 
  selectedDate,
  onBetClick,
  loading = false 
}: MatchTableProps) {
  
  // Time formatting is now handled by timeUtils

  const getStatusBadge = (match: Match) => {
    switch (match.status.toLowerCase()) {
      case 'live':
        return (
          <span className="flex items-center gap-2">
            <span className="w-2 h-2 bg-danger rounded-full animate-pulse"></span>
            <span className="text-danger font-bold bg-black/70 px-2 py-1 rounded">LIVE</span>
          </span>
        );
      case 'finished':
        return (
          <span className="text-text-muted text-sm">
            FT
          </span>
        );
      case 'postponed':
        return (
          <span className="text-warning text-xs font-semibold bg-black/70 px-2 py-1 rounded">
            POSTPONED
          </span>
        );
      case 'cancelled':
        return (
          <span className="text-danger text-xs font-semibold bg-black/70 px-2 py-1 rounded">
            CANCELLED
          </span>
        );
      case 'suspended':
        return (
          <span className="text-warning text-xs font-semibold bg-black/70 px-2 py-1 rounded">
            SUSPENDED
          </span>
        );
      default:
        return (
          <span className="text-white font-bold bg-black/70 px-2 py-1 rounded">
            {formatMatchTime(match.scheduled_time)}
          </span>
        );
    }
  };

  const getScore = (match: Match) => {
    if (match.status.toLowerCase() === 'live' && match.home_score !== null) {
      return (
        <div className="text-cyan font-bold mt-1">
          {match.home_score} - {match.away_score}
        </div>
      );
    }
    if (match.status.toLowerCase() === 'finished' && match.home_score !== null) {
      return (
        <div className="text-text-muted text-sm mt-1">
          {match.home_score} - {match.away_score}
        </div>
      );
    }
    return null;
  };

  const isBettingDisabled = (match: Match) => {
    const status = match.status.toLowerCase();
    return status === 'cancelled' || status === 'finished' || status === 'postponed';
  };

  if (loading) {
    return (
      <div className="rounded-card overflow-hidden border border-white/10">
        <div className="px-6 py-3">
          <div className="h-6 w-48 rounded animate-pulse"></div>
        </div>
        <div className="p-6 space-y-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-16 rounded animate-pulse"></div>
          ))}
        </div>
      </div>
    );
  }

  if (matches.length === 0) {
    return (
      <div className="rounded-card overflow-hidden border border-white/10">
        <div className="px-6 py-3 border-b border-white/10">
          <h2 className="text-white font-bold text-lg" style={{ textShadow: '0 4px 6px rgba(0, 0, 139, 0.8), 0 2px 4px rgba(0, 0, 139, 0.6)' }}>
            Matches - {new Date(selectedDate).toLocaleDateString('en-US', { 
              weekday: 'long', 
              year: 'numeric', 
              month: 'long', 
              day: 'numeric' 
            })}
          </h2>
        </div>
        <div className="p-12 text-center">
          <div className="text-6xl mb-4">⚽</div>
          <p className="text-white text-lg font-semibold" style={{ textShadow: '0 4px 6px rgba(0, 0, 139, 0.8), 0 2px 4px rgba(0, 0, 139, 0.6)' }}>No matches scheduled for this date</p>
          <p className="text-gray-300 text-sm mt-2 font-medium">Try selecting a different date or league</p>
        </div>
      </div>
    );
  }

  return (
    <div className="rounded-card overflow-hidden border border-white/10">
      {/* Table Header */}
      <div className="px-4 py-2 border-b border-white/10">
        <h2 className="text-white font-bold text-sm" style={{ textShadow: '0 4px 6px rgba(0, 0, 139, 0.8), 0 2px 4px rgba(0, 0, 139, 0.6)' }}>
          Matches - {new Date(selectedDate).toLocaleDateString('en-US', { 
            weekday: 'long', 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
          })}
        </h2>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr>
              <th className="px-3 py-2 text-left text-white text-xs font-bold" style={{ textShadow: '0 4px 6px rgba(0, 0, 139, 0.8), 0 2px 4px rgba(0, 0, 139, 0.6)' }}>
                Time
              </th>
              <th className="px-3 py-2 text-left text-white text-xs font-bold" style={{ textShadow: '0 4px 6px rgba(0, 0, 139, 0.8), 0 2px 4px rgba(0, 0, 139, 0.6)' }}>
                Match
              </th>
              <th className="px-3 py-2 text-left text-white text-xs font-bold" style={{ textShadow: '0 4px 6px rgba(0, 0, 139, 0.8), 0 2px 4px rgba(0, 0, 139, 0.6)' }}>
                League
              </th>
              <th className="px-3 py-2 text-center text-white text-xs font-bold" style={{ textShadow: '0 4px 6px rgba(0, 0, 139, 0.8), 0 2px 4px rgba(0, 0, 139, 0.6)' }}>
                1 (Home)
              </th>
              <th className="px-3 py-2 text-center text-white text-xs font-bold" style={{ textShadow: '0 4px 6px rgba(0, 0, 139, 0.8), 0 2px 4px rgba(0, 0, 139, 0.6)' }}>
                X (Draw)
              </th>
              <th className="px-3 py-2 text-center text-white text-xs font-bold" style={{ textShadow: '0 4px 6px rgba(0, 0, 139, 0.8), 0 2px 4px rgba(0, 0, 139, 0.6)' }}>
                2 (Away)
              </th>
              <th className="px-3 py-2 text-center text-white text-xs font-bold" style={{ textShadow: '0 4px 6px rgba(0, 0, 139, 0.8), 0 2px 4px rgba(0, 0, 139, 0.6)' }}>
                Actions
              </th>
            </tr>
          </thead>
          <tbody>
            {matches.map((match, index) => {
              const bettingDisabled = isBettingDisabled(match);
              
              return (
                <tr 
                  key={match.id}
                  className={`border-b border-white/10 transition-colors ${
                    bettingDisabled ? 'opacity-60' : ''
                  }`}
                >
                  {/* Time/Status Column */}
                  <td className="px-3 py-2 text-white whitespace-nowrap text-xs">
                    {getStatusBadge(match)}
                  </td>

                  {/* Match Column */}
                  <td className="px-3 py-2">
                    <div className="flex items-center gap-2">
                      {/* Team Logos */}
                      <div className="flex items-center gap-1.5">
                        {match.home_team_logo && (
                          <img 
                            src={match.home_team_logo} 
                            alt={match.home_team}
                            className="w-5 h-5 object-contain"
                            loading="lazy"
                            onError={(e) => e.currentTarget.style.display = 'none'}
                          />
                        )}
                        <span className="text-white font-semibold text-xs bg-black/70 px-2 py-1 rounded">
                          {match.home_team}
                        </span>
                      </div>
                      
                      <span className="text-gray-300 font-medium text-xs bg-black/70 px-2 py-1 rounded">vs</span>
                      
                      <div className="flex items-center gap-1.5">
                        {match.away_team_logo && (
                          <img 
                            src={match.away_team_logo} 
                            alt={match.away_team}
                            className="w-5 h-5 object-contain"
                            loading="lazy"
                            onError={(e) => e.currentTarget.style.display = 'none'}
                          />
                        )}
                        <span className="text-white font-semibold text-xs bg-black/70 px-2 py-1 rounded">
                          {match.away_team}
                        </span>
                      </div>
                    </div>
                    {getScore(match)}
                  </td>

                  {/* League Column */}
                  <td className="px-3 py-2">
                    <div className="flex items-center gap-2">
                      {match.league?.logo && (
                        <img 
                          src={match.league.logo} 
                          alt={match.league.name}
                          className="w-5 h-5 object-contain"
                          loading="lazy"
                          onError={(e) => e.currentTarget.style.display = 'none'}
                        />
                      )}
                      <div>
                        <div className="text-white text-xs font-semibold bg-black/70 px-2 py-1 rounded inline-block">
                          {match.league?.name || 'N/A'}
                        </div>
                        {match.league?.country && (
                          <div className="text-gray-300 text-[10px] font-medium mt-0.5 bg-black/70 px-2 py-1 rounded inline-block">
                            {match.league.country}
                          </div>
                        )}
                      </div>
                    </div>
                  </td>

                  {/* Home Odds */}
                  <td className="px-3 py-2 text-center">
                    <button 
                      onClick={() => !bettingDisabled && onBetClick?.(match, 'home')}
                      disabled={bettingDisabled}
                      className={`px-2 py-1 rounded font-semibold text-xs transition-all ${
                        bettingDisabled
                          ? 'bg-navy-300 text-text-muted cursor-not-allowed'
                          : 'bg-primary hover:bg-primary-600 text-white hover:scale-105'
                      }`}
                      aria-label={`Bet on ${match.home_team} at ${match.home_odds.toFixed(2)}`}
                    >
                      {match.home_odds.toFixed(2)}
                    </button>
                  </td>

                  {/* Draw Odds */}
                  <td className="px-3 py-2 text-center">
                    <button 
                      onClick={() => !bettingDisabled && onBetClick?.(match, 'draw')}
                      disabled={bettingDisabled}
                      className={`px-2 py-1 rounded font-semibold text-xs transition-all ${
                        bettingDisabled
                          ? 'bg-navy-300 text-text-muted cursor-not-allowed'
                          : 'bg-primary hover:bg-primary-600 text-white hover:scale-105'
                      }`}
                      aria-label={`Bet on draw at ${match.draw_odds.toFixed(2)}`}
                    >
                      {match.draw_odds.toFixed(2)}
                    </button>
                  </td>

                  {/* Away Odds */}
                  <td className="px-3 py-2 text-center">
                    <button 
                      onClick={() => !bettingDisabled && onBetClick?.(match, 'away')}
                      disabled={bettingDisabled}
                      className={`px-3 py-1.5 rounded font-semibold text-sm transition-all ${
                        bettingDisabled
                          ? 'bg-navy-300 text-text-muted cursor-not-allowed'
                          : 'bg-primary hover:bg-primary-600 text-white hover:scale-105'
                      }`}
                      aria-label={`Bet on ${match.away_team} at ${match.away_odds.toFixed(2)}`}
                    >
                      {match.away_odds.toFixed(2)}
                    </button>
                  </td>

                  {/* Actions Column */}
                  <td className="px-4 py-4 text-center">
                    <div className="flex items-center justify-center gap-2">
                      {match.status.toLowerCase() === 'live' && (
                        <Link
                          href={`/match/${match.id}`}
                          className="px-4 py-2 bg-danger hover:bg-danger/90 text-white rounded font-semibold text-sm transition-all inline-flex items-center gap-2"
                        >
                          <span className="w-2 h-2 bg-white rounded-full animate-pulse"></span>
                          Watch Live
                        </Link>
                      )}
                      {match.status.toLowerCase() === 'scheduled' && (
                        <Link
                          href={`/match/${match.id}`}
                          className="px-4 py-2 bg-danger hover:bg-danger/90 text-white rounded font-semibold text-sm transition-all"
                        >
                          Stream
                        </Link>
                      )}
                      {(match.status.toLowerCase() === 'finished' || 
                        match.status.toLowerCase() === 'cancelled' ||
                        match.status.toLowerCase() === 'postponed') && (
                        <Link
                          href={`/match/${match.id}`}
                          className="px-4 py-2 bg-navy-300 hover:bg-navy-400 text-text-muted rounded font-semibold text-sm transition-all"
                        >
                          View
                        </Link>
                      )}
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Table Footer with Match Count */}
      <div className="px-6 py-3 text-sm text-white font-semibold border-t border-white/10">
        Showing {matches.length} {matches.length === 1 ? 'match' : 'matches'}
      </div>
    </div>
  );
}
