'use client';

import MatchCard from './MatchCard';

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

interface MatchCardListProps {
  matches: Match[];
  selectedDate: string;
  onBetClick?: (match: Match, betType: 'home' | 'draw' | 'away') => void;
  loading?: boolean;
}

export default function MatchCardList({ 
  matches, 
  selectedDate,
  onBetClick,
  loading = false 
}: MatchCardListProps) {
  
  if (loading) {
    return (
      <div className="space-y-4">
        {[1, 2, 3].map((i) => (
          <div key={i} className="rounded-card h-64 animate-pulse border border-white/10"></div>
        ))}
      </div>
    );
  }

  if (matches.length === 0) {
    return (
      <div className="rounded-card p-8 text-center border border-white/10">
        <div className="text-6xl mb-4">⚽</div>
        <h3 className="text-text-primary text-lg font-semibold mb-2">
          No Matches Found
        </h3>
        <p className="text-text-muted">
          No matches scheduled for {new Date(selectedDate).toLocaleDateString('en-US', { 
            month: 'long', 
            day: 'numeric',
            year: 'numeric'
          })}
        </p>
        <p className="text-text-muted text-sm mt-2">
          Try selecting a different date or league
        </p>
      </div>
    );
  }

  return (
    <div>
      {/* Header */}
      <div className="mb-4 px-2">
        <h2 className="text-text-primary font-bold text-lg">
          {new Date(selectedDate).toLocaleDateString('en-US', { 
            weekday: 'long', 
            month: 'long', 
            day: 'numeric' 
          })}
        </h2>
        <p className="text-text-muted text-sm">
          {matches.length} {matches.length === 1 ? 'match' : 'matches'}
        </p>
      </div>

      {/* Match Cards Grid */}
      <div className="grid grid-cols-1 gap-4">
        {matches.map((match) => (
          <MatchCard 
            key={match.id} 
            match={match}
            onBetClick={onBetClick}
          />
        ))}
      </div>
    </div>
  );
}
