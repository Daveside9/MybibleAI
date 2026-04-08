'use client';

interface League {
  id: number;
  name: string;
  country: string;
  match_count: number;
  logo?: string;
}

interface LeagueFilterProps {
  leagues: League[];
  selectedLeague: number | null;
  onLeagueChange: (leagueId: number | null) => void;
  loading?: boolean;
}

export default function LeagueFilter({ 
  leagues, 
  selectedLeague, 
  onLeagueChange,
  loading = false 
}: LeagueFilterProps) {
  
  if (loading) {
    return (
      <div className="bg-navy-100 rounded-card p-4">
        <h3 className="text-text-primary font-semibold mb-3">Filter by League</h3>
        <div className="flex gap-2 flex-wrap">
          <div className="h-10 w-32 bg-navy-200 rounded-lg animate-pulse"></div>
          <div className="h-10 w-40 bg-navy-200 rounded-lg animate-pulse"></div>
          <div className="h-10 w-36 bg-navy-200 rounded-lg animate-pulse"></div>
        </div>
      </div>
    );
  }

  if (leagues.length === 0) {
    return null;
  }

  // Sort leagues by match count (descending) and then by name
  const sortedLeagues = [...leagues].sort((a, b) => {
    if (b.match_count !== a.match_count) {
      return b.match_count - a.match_count;
    }
    return a.name.localeCompare(b.name);
  });

  const totalMatches = leagues.reduce((sum, league) => sum + league.match_count, 0);

  return (
    <div className="bg-navy-100 rounded-card p-4">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-text-primary font-semibold">Filter by League</h3>
        <span className="text-text-muted text-sm">
          {leagues.length} {leagues.length === 1 ? 'league' : 'leagues'}
        </span>
      </div>
      
      <div className="flex gap-2 flex-wrap">
        {/* All Leagues Button */}
        <button
          onClick={() => onLeagueChange(null)}
          className={`
            px-4 py-2 rounded-lg transition-all font-medium text-sm
            ${selectedLeague === null
              ? 'bg-primary text-white shadow-lg'
              : 'bg-navy-200 text-text-muted hover:bg-navy-300 hover:text-text-primary'
            }
          `}
          aria-pressed={selectedLeague === null}
          aria-label={`Show all leagues (${totalMatches} matches)`}
        >
          <span className="flex items-center gap-2">
            <span>All Leagues</span>
            <span className={`
              text-xs px-2 py-0.5 rounded-full
              ${selectedLeague === null 
                ? 'bg-white/20 text-white' 
                : 'bg-navy-300 text-text-muted'
              }
            `}>
              {totalMatches}
            </span>
          </span>
        </button>

        {/* Individual League Buttons */}
        {sortedLeagues.map((league) => (
          <button
            key={league.id}
            onClick={() => onLeagueChange(league.id)}
            className={`
              px-4 py-2 rounded-lg transition-all font-medium text-sm
              ${selectedLeague === league.id
                ? 'bg-primary text-white shadow-lg'
                : 'bg-navy-200 text-text-muted hover:bg-navy-300 hover:text-text-primary'
              }
            `}
            aria-pressed={selectedLeague === league.id}
            aria-label={`Filter by ${league.name} (${league.match_count} matches)`}
          >
            <span className="flex items-center gap-2">
              {/* League Logo (if available) */}
              {league.logo && (
                <img 
                  src={league.logo} 
                  alt={`${league.name} logo`}
                  className="w-4 h-4 object-contain"
                  onError={(e) => {
                    // Hide image if it fails to load
                    e.currentTarget.style.display = 'none';
                  }}
                />
              )}
              
              {/* League Name */}
              <span className="truncate max-w-[200px]">
                {league.name}
              </span>
              
              {/* Match Count Badge */}
              <span className={`
                text-xs px-2 py-0.5 rounded-full flex-shrink-0
                ${selectedLeague === league.id 
                  ? 'bg-white/20 text-white' 
                  : 'bg-navy-300 text-text-muted'
                }
              `}>
                {league.match_count}
              </span>
            </span>
          </button>
        ))}
      </div>

      {/* Selected League Info */}
      {selectedLeague !== null && (
        <div className="mt-3 pt-3 border-t border-navy-200">
          <div className="text-sm text-text-muted">
            Showing {sortedLeagues.find(l => l.id === selectedLeague)?.match_count || 0} matches from{' '}
            <span className="text-text-primary font-semibold">
              {sortedLeagues.find(l => l.id === selectedLeague)?.name}
            </span>
          </div>
        </div>
      )}

      {/* Screen reader announcement */}
      <div className="sr-only" role="status" aria-live="polite">
        {selectedLeague === null 
          ? `Showing all ${totalMatches} matches from ${leagues.length} leagues`
          : `Filtered to ${sortedLeagues.find(l => l.id === selectedLeague)?.name} with ${sortedLeagues.find(l => l.id === selectedLeague)?.match_count} matches`
        }
      </div>
    </div>
  );
}
