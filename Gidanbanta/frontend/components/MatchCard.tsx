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

interface MatchCardProps {
  match: Match;
  onBetClick?: (match: Match, betType: 'home' | 'draw' | 'away') => void;
}

export default function MatchCard({ match, onBetClick }: MatchCardProps) {
  // Time formatting is now handled by timeUtils

  const getStatusBadge = () => {
    switch (match.status.toLowerCase()) {
      case 'live':
        return (
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 bg-danger rounded-full animate-pulse"></span>
            <span className="text-danger font-bold text-sm bg-black/70 px-2 py-1 rounded">LIVE</span>
          </div>
        );
      case 'finished':
        return (
          <div>
            <span className="text-text-muted text-sm font-semibold bg-black/70 px-2 py-1 rounded">FT</span>
          </div>
        );
      case 'postponed':
        return (
          <div>
            <span className="text-warning text-xs font-semibold bg-black/70 px-2 py-1 rounded">POSTPONED</span>
          </div>
        );
      case 'cancelled':
        return (
          <div>
            <span className="text-danger text-xs font-semibold bg-black/70 px-2 py-1 rounded">CANCELLED</span>
          </div>
        );
      case 'suspended':
        return (
          <div>
            <span className="text-warning text-xs font-semibold bg-black/70 px-2 py-1 rounded">SUSPENDED</span>
          </div>
        );
      default:
        return (
          <div>
            <span className="text-white text-sm font-bold bg-black/70 px-2 py-1 rounded" style={{ textShadow: '0 4px 6px rgba(0, 0, 139, 0.8), 0 2px 4px rgba(0, 0, 139, 0.6)' }}>
              {formatMatchTime(match.scheduled_time)}
            </span>
          </div>
        );
    }
  };

  const getScore = () => {
    if (match.status.toLowerCase() === 'live' && match.home_score !== null) {
      return (
        <div className="text-3xl font-bold text-cyan">
          {match.home_score} - {match.away_score}
        </div>
      );
    }
    if (match.status.toLowerCase() === 'finished' && match.home_score !== null) {
      return (
        <div className="text-2xl font-bold text-text-muted">
          {match.home_score} - {match.away_score}
        </div>
      );
    }
    return (
      <div className="text-2xl font-bold text-text-muted">
        vs
      </div>
    );
  };

  const isBettingDisabled = () => {
    const status = match.status.toLowerCase();
    return status === 'cancelled' || status === 'finished' || status === 'postponed';
  };

  const bettingDisabled = isBettingDisabled();

  return (
    <div className={`rounded-card overflow-hidden border border-white/10 ${
      bettingDisabled ? 'opacity-60' : ''
    }`}>
      {/* Card Header - League Info */}
      <div className="px-4 py-2 flex items-center justify-between border-b border-white/10">
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
            <div className="text-white text-sm font-bold bg-black/70 px-2 py-1 rounded inline-block">
              {match.league?.name || 'League'}
            </div>
            {match.league?.country && (
              <div className="text-gray-300 text-xs font-semibold mt-1 bg-black/70 px-2 py-1 rounded inline-block">
                {match.league.country}
              </div>
            )}
          </div>
        </div>
        {getStatusBadge()}
      </div>

      {/* Card Body - Match Info */}
      <div className="p-4">
        {/* Teams */}
        <div className="flex items-center justify-between mb-4">
          {/* Home Team */}
          <div className="flex-1 flex flex-col items-center">
            {match.home_team_logo && (
              <img 
                src={match.home_team_logo} 
                alt={match.home_team}
                className="w-12 h-12 object-contain mb-2"
                loading="lazy"
                onError={(e) => e.currentTarget.style.display = 'none'}
              />
            )}
            <div className="text-white font-bold text-center text-sm bg-black/70 px-2 py-1 rounded">
              {match.home_team}
            </div>
          </div>

          {/* Score/VS */}
          <div className="flex-shrink-0 px-4">
            {getScore()}
          </div>

          {/* Away Team */}
          <div className="flex-1 flex flex-col items-center">
            {match.away_team_logo && (
              <img 
                src={match.away_team_logo} 
                alt={match.away_team}
                className="w-12 h-12 object-contain mb-2"
                loading="lazy"
                onError={(e) => e.currentTarget.style.display = 'none'}
              />
            )}
            <div className="text-white font-bold text-center text-sm bg-black/70 px-2 py-1 rounded">
              {match.away_team}
            </div>
          </div>
        </div>

        {/* Betting Odds */}
        <div className="grid grid-cols-3 gap-2 mb-3">
          {/* Home Odds */}
          <button
            onClick={() => !bettingDisabled && onBetClick?.(match, 'home')}
            disabled={bettingDisabled}
            className={`
              py-3 rounded-lg transition-all
              ${bettingDisabled
                ? 'bg-navy-300 text-text-muted cursor-not-allowed'
                : 'bg-primary hover:bg-primary-600 text-white active:scale-95'
              }
            `}
            style={{ minHeight: '48px' }} // Touch target size
            aria-label={`Bet on ${match.home_team} at ${match.home_odds.toFixed(2)}`}
          >
            <div className="text-xs opacity-80 mb-1">Home</div>
            <div className="text-lg font-bold">{match.home_odds.toFixed(2)}</div>
          </button>

          {/* Draw Odds */}
          <button
            onClick={() => !bettingDisabled && onBetClick?.(match, 'draw')}
            disabled={bettingDisabled}
            className={`
              py-3 rounded-lg transition-all
              ${bettingDisabled
                ? 'bg-navy-300 text-text-muted cursor-not-allowed'
                : 'bg-primary hover:bg-primary-600 text-white active:scale-95'
              }
            `}
            style={{ minHeight: '48px' }} // Touch target size
            aria-label={`Bet on draw at ${match.draw_odds.toFixed(2)}`}
          >
            <div className="text-xs opacity-80 mb-1">Draw</div>
            <div className="text-lg font-bold">{match.draw_odds.toFixed(2)}</div>
          </button>

          {/* Away Odds */}
          <button
            onClick={() => !bettingDisabled && onBetClick?.(match, 'away')}
            disabled={bettingDisabled}
            className={`
              py-3 rounded-lg transition-all
              ${bettingDisabled
                ? 'bg-navy-300 text-text-muted cursor-not-allowed'
                : 'bg-primary hover:bg-primary-600 text-white active:scale-95'
              }
            `}
            style={{ minHeight: '48px' }} // Touch target size
            aria-label={`Bet on ${match.away_team} at ${match.away_odds.toFixed(2)}`}
          >
            <div className="text-xs opacity-80 mb-1">Away</div>
            <div className="text-lg font-bold">{match.away_odds.toFixed(2)}</div>
          </button>
        </div>

        {/* Action Button */}
        <div>
          {match.status.toLowerCase() === 'live' && (
            <Link
              href={`/match/${match.id}`}
              className="block w-full py-3 bg-danger hover:bg-danger/90 text-white rounded-lg font-semibold text-center transition-all active:scale-95"
              style={{ minHeight: '48px' }} // Touch target size
            >
              <span className="flex items-center justify-center gap-2">
                <span className="w-2 h-2 bg-white rounded-full animate-pulse"></span>
                Watch Live
              </span>
            </Link>
          )}
          {match.status.toLowerCase() === 'scheduled' && (
            <Link
              href={`/match/${match.id}`}
              className="block w-full py-3 bg-danger hover:bg-danger/90 text-white rounded-lg font-semibold text-center transition-all active:scale-95"
              style={{ minHeight: '48px' }} // Touch target size
            >
              Stream
            </Link>
          )}
          {(match.status.toLowerCase() === 'finished' || 
            match.status.toLowerCase() === 'cancelled' ||
            match.status.toLowerCase() === 'postponed') && (
            <Link
              href={`/match/${match.id}`}
              className="block w-full py-3 bg-navy-300 hover:bg-navy-400 text-text-muted rounded-lg font-semibold text-center transition-all active:scale-95"
              style={{ minHeight: '48px' }} // Touch target size
            >
              View Match
            </Link>
          )}
        </div>
      </div>
    </div>
  );
}
