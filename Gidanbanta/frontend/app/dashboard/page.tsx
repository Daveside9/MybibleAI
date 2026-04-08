'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuth } from '@/contexts/AuthContext';
import { api } from '@/lib/api';
import dynamic from 'next/dynamic';
import MatchTable from '@/components/MatchTable';
import MatchCardList from '@/components/MatchCardList';
import AccountDropdown from '@/components/AccountDropdown';
import BetslipWidget from '@/components/BetslipWidget';
import DatePicker from '@/components/DatePicker';

// Lazy load BettingModal for code splitting
const BettingModal = dynamic(() => import('@/components/BettingModal'), {
  ssr: false,
  loading: () => null
});

interface CalendarMatch {
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
  } | null;
}

interface Wallet {
  balance: number;
  deposited_amount: number;
  winnings_amount: number;
}

interface League {
  id: number;
  name: string;
  country: string;
  match_count: number;
}

interface BetSelection {
  matchId: number;
  homeTeam: string;
  awayTeam: string;
  betType: 'home' | 'draw' | 'away';
  odds: number;
  league: string;
}

export default function DashboardPage() {
  const { user, loading: authLoading, logout } = useAuth();
  const router = useRouter();
  const [matches, setMatches] = useState<CalendarMatch[]>([]);
  const [wallet, setWallet] = useState<Wallet | null>(null);
  const [leagues, setLeagues] = useState<League[]>([]);
  const [selectedDate, setSelectedDate] = useState<string>(new Date().toISOString().split('T')[0]);
  const [selectedLeague, setSelectedLeague] = useState<number | null>(null);
  const [selectedStatus, setSelectedStatus] = useState<string | null>(null);
  const [showMatches, setShowMatches] = useState(false);
  const [loading, setLoading] = useState(true);
  const [matchesLoading, setMatchesLoading] = useState(false);
  const [error, setError] = useState<string>('');
  const [bettingModalOpen, setBettingModalOpen] = useState(false);
  const [selectedMatch, setSelectedMatch] = useState<CalendarMatch | null>(null);
  const [selectedBetType, setSelectedBetType] = useState<'home' | 'draw' | 'away'>('home');
  const [currentAdIndex, setCurrentAdIndex] = useState(0);
  const [bottomMenuOpen, setBottomMenuOpen] = useState(false);
  const [activeBottomTab, setActiveBottomTab] = useState<'quick-access' | 'betslip' | 'my-bets'>('quick-access');
  const [betslipItems, setBetslipItems] = useState<any[]>([]);
  const [myBets, setMyBets] = useState<any[]>([]);
  const [betSelections, setBetSelections] = useState<BetSelection[]>([]);

  useEffect(() => {
    if (!authLoading && !user) {
      router.push('/login');
    } else if (user) {
      loadData();
    }
  }, [user, authLoading, router]);

  useEffect(() => {
    if (user && selectedDate && showMatches) {
      loadMatches();
    }
  }, [selectedDate, selectedLeague, selectedStatus, showMatches]);

  // Auto-slide advertisement banner every 8 seconds
  useEffect(() => {
    const adInterval = setInterval(() => {
      setCurrentAdIndex((prevIndex) => (prevIndex + 1) % 6); // 6 different ad sets
    }, 8000);

    return () => clearInterval(adInterval);
  }, []);

  const loadData = async () => {
    setLoading(true);
    setError('');
    
    try {
      // Load wallet and leagues in parallel for faster loading
      const today = selectedDate;
      const endDate = selectedDate;
      
      const [walletResponse, leaguesResponse] = await Promise.all([
        api.getWallet(),
        api.getAvailableLeagues(today, endDate)
      ]);

      if (walletResponse.data) {
        setWallet(walletResponse.data as Wallet);
      } else if (walletResponse.error) {
        console.error('Wallet error:', walletResponse.error);
      }

      if (leaguesResponse.data) {
        setLeagues(leaguesResponse.data as League[]);
      } else if (leaguesResponse.error) {
        console.error('Leagues error:', leaguesResponse.error);
      }
    } catch (err: any) {
      console.error('Error loading data:', err);
      setError(err.message || 'Failed to load data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const loadMatches = async () => {
    const today = selectedDate;
    const endDate = selectedDate;

    try {
      setMatchesLoading(true);
      setError('');
      
      // Always load both matches and leagues to ensure proper filtering
      const [matchesResponse, leaguesResponse] = await Promise.all([
        api.getCalendarMatches({
          start_date: today,
          end_date: endDate,
          league_id: selectedLeague || undefined
        }),
        api.getAvailableLeagues(today, endDate)
      ]);

      if (matchesResponse.data) {
        const data = matchesResponse.data as any;
        setMatches(data.matches || []);
      } else if (matchesResponse.error) {
        console.error('Matches error:', matchesResponse.error);
        setError('Failed to load matches. Please try again.');
      }

      if (leaguesResponse.data) {
        setLeagues(leaguesResponse.data as League[]);
      } else if (leaguesResponse.error) {
        console.error('Leagues error:', leaguesResponse.error);
      }
    } catch (err: any) {
      console.error('Error loading matches:', err);
      setError(err.message || 'Failed to load matches. Please try again.');
    } finally {
      setMatchesLoading(false);
    }
  };

  // Filter matches based on selected status
  const filteredMatches = selectedStatus === 'live' 
    ? matches.filter(match => match.status.toLowerCase() === 'live')
    : matches;

  const handleBetClick = (match: CalendarMatch, betType: 'home' | 'draw' | 'away') => {
    // Check if this match is already in betslip
    const existingIndex = betSelections.findIndex(sel => sel.matchId === match.id);
    
    if (existingIndex >= 0) {
      // Update existing selection
      const updated = [...betSelections];
      updated[existingIndex] = {
        matchId: match.id,
        homeTeam: match.home_team,
        awayTeam: match.away_team,
        betType,
        odds: betType === 'home' ? match.home_odds : betType === 'away' ? match.away_odds : match.draw_odds,
        league: match.league?.name || 'Unknown League'
      };
      setBetSelections(updated);
    } else {
      // Add new selection
      setBetSelections([...betSelections, {
        matchId: match.id,
        homeTeam: match.home_team,
        awayTeam: match.away_team,
        betType,
        odds: betType === 'home' ? match.home_odds : betType === 'away' ? match.away_odds : match.draw_odds,
        league: match.league?.name || 'Unknown League'
      }]);
    }
  };

  const handleRemoveSelection = (matchId: number) => {
    setBetSelections(betSelections.filter(sel => sel.matchId !== matchId));
  };

  const handleClearBetslip = () => {
    setBetSelections([]);
  };

  const handlePlaceBet = async (stake: number) => {
    // TODO: Implement actual bet placement API call
    console.log('Placing accumulator bet:', { 
      selections: betSelections, 
      stake,
      totalOdds: betSelections.reduce((acc, sel) => acc * sel.odds, 1)
    });
    
    // For now, just show success message and clear betslip
    alert(`Bet placed successfully!\nStake: ₦${stake}\nSelections: ${betSelections.length}`);
    setBetSelections([]);
    
    // In real implementation, this would:
    // 1. Call the betting API
    // 2. Update wallet balance
    // 3. Add to my bets list
  };

  const handleSingleBetClick = (match: CalendarMatch, betType: 'home' | 'draw' | 'away') => {
    setSelectedMatch(match);
    setSelectedBetType(betType);
    setBettingModalOpen(true);
  };

  const handlePlaceSingleBet = async (matchId: number, betType: 'home' | 'draw' | 'away', stake: number) => {
    // TODO: Implement actual bet placement API call
    console.log('Placing single bet:', { matchId, betType, stake });
    // For now, just close the modal
    // In real implementation, this would call the betting API
  };

  const handleTopUp = () => {
    router.push('/wallet');
  };

  if (authLoading || loading) {
    return (
      <div className="min-h-screen bg-navy flex items-center justify-center">
        <div className="text-text-primary text-xl">Loading...</div>
      </div>
    );
  }

  if (!user) {
    return null;
  }

  return (
    <div className="h-screen w-screen bg-navy relative overflow-hidden flex flex-col">
      {/* Main Content Area - Full Screen */}
      <div className="relative overflow-hidden flex-1 flex flex-col w-full">
        {/* Animated Football Background */}
        <div className="fixed inset-0 z-0">
          <div 
            className="absolute inset-0 bg-center"
            style={{
              backgroundImage: "url('https://wallpapers.com/images/high/uefa-champions-league-intergalactic-stadium-2mxl696eobodolq3.webp')",
              backgroundSize: "cover",
              backgroundRepeat: "no-repeat"
            }}
          ></div>
          <div className="absolute inset-0 bg-gradient-to-b from-black/40 via-black/30 to-black/50"></div>
        </div>
        
        {/* Floating football icons animation */}
        <div className="fixed inset-0 z-0 pointer-events-none">
          <div className="absolute top-20 left-10 text-6xl opacity-10 animate-bounce" style={{ animationDelay: '0s', animationDuration: '3s' }}></div>
          <div className="absolute top-40 right-20 text-5xl opacity-10 animate-bounce" style={{ animationDelay: '1s', animationDuration: '4s' }}></div>
          <div className="absolute bottom-32 left-1/4 text-7xl opacity-10 animate-bounce" style={{ animationDelay: '2s', animationDuration: '5s' }}></div>
          <div className="absolute bottom-20 right-1/3 text-6xl opacity-10 animate-bounce" style={{ animationDelay: '1.5s', animationDuration: '3.5s' }}></div>
        </div>

      {/* Header - Dark Shining 3D Style */}
      <header className="bg-black/20 backdrop-blur-md shadow-2xl relative z-[60] border-b border-white/10 w-full flex-shrink-0">
        {/* Top Bar - Logo, Amount, Account */}
        <div className="w-full px-2 sm:px-3 py-1">
          <div className="flex items-center justify-between gap-2">
            {/* Left - Empty spacer for balance */}
            <div className="flex-shrink-0 w-20 sm:w-24"></div>

            {/* Center - GidanBanta Logo */}
            <div className="flex-1 flex justify-center">
              <button
                onClick={() => {
                  setShowMatches(false);
                  setSelectedLeague(null);
                  setSelectedStatus(null);
                  setSelectedDate(new Date().toISOString().split('T')[0]);
                }}
                className="cursor-pointer hover:scale-105 transition-transform"
              >
                <h1 className="text-lg sm:text-xl md:text-2xl font-heading font-bold italic bg-gradient-to-r from-gray-300 via-gray-200 to-gray-400 bg-clip-text text-transparent" style={{ textShadow: '0 4px 6px rgba(0, 0, 139, 0.8), 0 2px 4px rgba(0, 0, 139, 0.6)' }}>
                  GidanBanta
                </h1>
              </button>
            </div>

            {/* Right - Wallet & Account */}
            <div className="flex items-center gap-1 flex-shrink-0">
              {/* Wallet Balance */}
              <Link href="/wallet" className="bg-black/30 hover:bg-black/40 backdrop-blur-md px-2 py-1 rounded-lg border border-white/20 shadow-lg transition-all">
                <div className="flex items-center gap-1">
                  <div className="text-white">
                    <div className="text-xs sm:text-sm font-bold whitespace-nowrap">
                      ₦{wallet?.balance.toFixed(2) || '0.00'}
                    </div>
                  </div>
                  <div className="text-sm sm:text-base">💰</div>
                </div>
              </Link>

              {/* Account Dropdown */}
              <AccountDropdown user={user} onLogout={logout} onTopUp={handleTopUp} />
            </div>
          </div>
        </div>

        {/* Navigation Bar */}
        <div className="border-t border-white/10 bg-black/10 backdrop-blur-sm w-full">
          <div className="w-full mx-auto px-2 sm:px-4 py-1">
            <div className="flex flex-col items-center gap-2">
              {/* Main Navigation */}
              <nav className="flex items-center gap-1 bg-black/20 backdrop-blur-md rounded-lg p-1 border border-white/10 shadow-lg">
                <Link href="/dashboard" className="px-4 py-1.5 bg-gradient-to-r from-gray-600 to-gray-700 text-white text-sm font-semibold rounded-md transition-all hover:from-gray-500 hover:to-gray-600 shadow-md transform hover:scale-105">
                  Matches
                </Link>
                <Link href="/fantasy" className="px-4 py-1.5 text-sm text-white/80 hover:text-white hover:bg-gradient-to-r hover:from-gray-700 hover:to-gray-800 rounded-md transition-all">
                  Fantasy
                </Link>
              </nav>

              {/* Date Picker and League Navigation */}
              <div className="flex items-center gap-2 flex-wrap">
                {/* Date Picker */}
                <DatePicker 
                  selectedDate={selectedDate}
                  onDateChange={(date) => {
                    setSelectedDate(date);
                    setShowMatches(true);
                  }}
                />
                
                {/* League Navigation */}
                <nav className="flex items-center gap-1 bg-black/20 backdrop-blur-md rounded-lg p-1 border border-white/10 overflow-x-auto max-w-full shadow-lg">
                <button 
                  onClick={() => {
                    setSelectedLeague(null);
                    setSelectedStatus(null);
                    setShowMatches(true);
                  }}
                  disabled={matchesLoading}
                  className={`px-3 py-1.5 text-sm font-medium rounded-md transition-all whitespace-nowrap transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed ${
                    selectedLeague === null && selectedStatus === null && showMatches
                      ? 'bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-lg' 
                      : 'text-gray-300 hover:bg-gradient-to-r hover:from-gray-700 hover:to-gray-800 hover:text-white'
                  }`}
                  style={selectedLeague === null && selectedStatus === null && showMatches ? {
                    boxShadow: 'inset 0 1px 0 rgba(255,255,255,0.2), 0 4px 15px rgba(59, 130, 246, 0.3)',
                  } : {}}
                >
                  {matchesLoading && selectedLeague === null && selectedStatus === null ? (
                    <span className="flex items-center gap-1">
                      <div className="w-3 h-3 border border-white border-t-transparent rounded-full animate-spin"></div>
                      Loading...
                    </span>
                  ) : (
                    'All Leagues'
                  )}
                </button>
                <button 
                  onClick={() => {
                    setSelectedLeague(null);
                    setSelectedStatus('live');
                    setShowMatches(true);
                  }}
                  className={`px-3 py-1.5 text-sm font-medium rounded-md transition-all whitespace-nowrap transform hover:scale-105 ${
                    selectedStatus === 'live' && showMatches
                      ? 'bg-gradient-to-r from-red-600 to-red-700 text-white shadow-lg' 
                      : 'text-gray-300 hover:bg-gradient-to-r hover:from-gray-700 hover:to-gray-800 hover:text-white'
                  }`}
                  style={selectedStatus === 'live' && showMatches ? {
                    boxShadow: 'inset 0 1px 0 rgba(255,255,255,0.2), 0 4px 15px rgba(220, 38, 38, 0.3)',
                  } : {}}
                >
                  🔴 Live
                </button>
                {leagues.slice(0, 8).map((league) => (
                  <button
                    key={league.id}
                    onClick={() => {
                      setSelectedLeague(league.id);
                      setSelectedStatus(null);
                      setShowMatches(true);
                    }}
                    disabled={matchesLoading}
                    className={`px-3 py-1.5 text-sm font-medium rounded-md transition-all whitespace-nowrap transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed ${
                      selectedLeague === league.id && showMatches
                        ? 'bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-lg'
                        : 'text-gray-300 hover:bg-gradient-to-r hover:from-gray-700 hover:to-gray-800 hover:text-white'
                    }`}
                    style={selectedLeague === league.id && showMatches ? {
                      boxShadow: 'inset 0 1px 0 rgba(255,255,255,0.2), 0 4px 15px rgba(59, 130, 246, 0.3)',
                    } : {}}
                  >
                    {matchesLoading && selectedLeague === league.id ? (
                      <span className="flex items-center gap-1">
                        <div className="w-3 h-3 border border-white border-t-transparent rounded-full animate-spin"></div>
                        Loading...
                      </span>
                    ) : (
                      league.name
                    )}
                  </button>
                ))}
                {leagues.length > 8 && (
                  <button className="px-2 py-1 text-xs font-medium text-gray-400 hover:bg-gradient-to-r hover:from-gray-700 hover:to-gray-800 hover:text-white rounded-md transition-all transform hover:scale-105">
                    +{leagues.length - 8} More
                  </button>
                )}
              </nav>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Advertisement Banner */}
      <div className="bg-black/20 backdrop-blur-md border-b border-white/10 w-full">
        <div className="w-full mx-auto px-2 py-1">
          <div className="flex items-center justify-center gap-4 text-white text-xs font-semibold">
            <span>🎁 Welcome Bonus: 100% up to ₦20,000</span>
            <span className="hidden md:inline">💰 10% Weekly Cashback</span>
            <span className="hidden lg:inline">⚽ Live Betting Available</span>
          </div>
        </div>
      </div>

      <div className="hidden">
        <div className="relative h-16 flex items-center">
          <div 
            className="flex transition-transform duration-500 ease-in-out" 
            style={{ transform: `translateX(-${currentAdIndex * 100}%)` }}
          >
            {/* Slide 1 - Welcome & Bonus Ads */}
            <div className="min-w-full px-4">
              <div className="flex items-center gap-4 overflow-x-auto pb-2">
                <div className="flex items-center gap-2 bg-gradient-to-r from-green-600 to-emerald-700 rounded-lg px-4 py-2 backdrop-blur-sm flex-shrink-0 border border-green-400/50 shadow-lg">
                  <div className="text-white">
                    <div className="text-xs font-bold text-green-100"> WELCOME BONUS</div>
                    <div className="text-sm font-extrabold">100% First Deposit</div>
                    <div className="text-xs font-semibold opacity-100">Up to ₦20,000</div>
                  </div>
                  <div className="text-lg"></div>
                </div>
                
                <div className="flex items-center gap-2 bg-gradient-to-r from-blue-600 to-cyan-600 rounded-lg px-4 py-2 backdrop-blur-sm flex-shrink-0 border border-blue-400/50 shadow-lg">
                  <div className="text-white">
                    <div className="text-xs font-bold text-blue-100"> CASHBACK</div>
                    <div className="text-sm font-extrabold">10% Weekly Cashback</div>
                    <div className="text-xs font-semibold opacity-100">Every Monday</div>
                  </div>
                  <div className="text-lg"></div>
                </div>

                <div className="flex items-center gap-2 bg-gradient-to-r from-purple-600 to-pink-600 rounded-lg px-4 py-2 backdrop-blur-sm flex-shrink-0 border border-purple-400/50 shadow-lg">
                  <div className="text-white">
                    <div className="text-xs font-bold text-purple-100"> VIP CLUB</div>
                    <div className="text-sm font-extrabold">Join VIP Program</div>
                    <div className="text-xs font-semibold opacity-100">Exclusive Rewards</div>
                  </div>
                  <div className="text-lg"></div>
                </div>

                <div className="flex items-center gap-2 bg-gradient-to-r from-red-600 to-orange-600 rounded-lg px-4 py-2 backdrop-blur-sm flex-shrink-0 border border-red-400/50 shadow-lg">
                  <div className="text-white">
                    <div className="text-xs font-bold text-red-100"> LIVE MATCH</div>
                    <div className="text-sm font-extrabold">Chelsea vs Arsenal</div>
                    <div className="text-xs font-semibold opacity-100">Odds: 2.15 vs 1.95</div>
                  </div>
                  <div className="text-lg"></div>
                </div>

                <div className="flex items-center gap-2 bg-gradient-to-r from-yellow-600 to-amber-600 rounded-lg px-4 py-2 backdrop-blur-sm flex-shrink-0 border border-yellow-400/50 shadow-lg">
                  <div className="text-white">
                    <div className="text-xs font-bold text-yellow-100"> ACCA BOOST</div>
                    <div className="text-sm font-extrabold">Accumulator Boost</div>
                    <div className="text-xs font-semibold opacity-100">Up to 70% Extra</div>
                  </div>
                  <div className="text-lg"></div>
                </div>
              </div>
            </div>

            {/* Slide 2 - Banta Room & Social Ads */}
            <div className="min-w-full px-4">
              <div className="flex items-center gap-3 overflow-x-auto pb-2">
                <div className="flex items-center gap-1.5 bg-gray-600/30 rounded px-2 py-1 backdrop-blur-sm flex-shrink-0 border border-gray-500/20">
                  <div className="text-white">
                    <div className="text-[9px] font-semibold text-gray-300"> BANTA ROOM</div>
                    <div className="text-[10px] font-bold">Visit Your Room</div>
                    <div className="text-[8px] opacity-90">Private Chat & Rewards</div>
                  </div>
                  <div className="text-2xl"></div>
                </div>

                <div className="flex items-center gap-1.5 bg-gray-600/30 rounded px-2 py-1 backdrop-blur-sm flex-shrink-0 border border-gray-500/20">
                  <div className="text-white">
                    <div className="text-[9px] font-semibold text-gray-300"> COMMUNITY</div>
                    <div className="text-[10px] font-bold">Join Chat Groups</div>
                    <div className="text-[8px] opacity-90">Connect with Fans</div>
                  </div>
                  <div className="text-2xl"></div>
                </div>

                <div className="flex items-center gap-1.5 bg-gray-600/30 rounded px-2 py-1 backdrop-blur-sm flex-shrink-0 border border-gray-500/20">
                  <div className="text-white">
                    <div className="text-[9px] font-semibold text-gray-300"> LEADERBOARD</div>
                    <div className="text-[10px] font-bold">Top Winners</div>
                    <div className="text-[8px] opacity-90">Weekly Rankings</div>
                  </div>
                  <div className="text-2xl"></div>
                </div>

                <div className="flex items-center gap-1.5 bg-gray-600/30 rounded px-2 py-1 backdrop-blur-sm flex-shrink-0 border border-gray-500/20">
                  <div className="text-white">
                    <div className="text-[9px] font-semibold text-gray-300"> DAILY BONUS</div>
                    <div className="text-[10px] font-bold">Login Rewards</div>
                    <div className="text-[8px] opacity-90">Claim Daily</div>
                  </div>
                  <div className="text-2xl"></div>
                </div>

                <div className="flex items-center gap-1.5 bg-gray-600/30 rounded px-2 py-1 backdrop-blur-sm flex-shrink-0 border border-gray-500/20">
                  <div className="text-white">
                    <div className="text-[9px] font-semibold text-gray-300"> PREMIER LEAGUE</div>
                    <div className="text-[10px] font-bold">Man City vs Liverpool</div>
                    <div className="text-[8px] opacity-90">Today 3:00 PM</div>
                  </div>
                  <div className="text-2xl"></div>
                </div>

                <div className="flex items-center gap-1.5 bg-gray-600/30 rounded px-2 py-1 backdrop-blur-sm flex-shrink-0 border border-gray-500/20">
                  <div className="text-white">
                    <div className="text-[9px] font-semibold text-gray-300"> LIVE BETTING</div>
                    <div className="text-[10px] font-bold">In-Play Betting</div>
                    <div className="text-[8px] opacity-90">Bet While Watching</div>
                  </div>
                  <div className="text-2xl"></div>
                </div>
              </div>
            </div>

            {/* Slide 3 - Live Streaming & Entertainment */}
            <div className="min-w-full px-4">
              <div className="flex items-center gap-3 overflow-x-auto pb-2">
                <div className="flex items-center gap-1.5 bg-gray-600/30 rounded px-2 py-1 backdrop-blur-sm flex-shrink-0 border border-gray-500/20">
                  <div className="text-white">
                    <div className="text-[9px] font-semibold text-gray-300"> LIVE STREAM</div>
                    <div className="text-[10px] font-bold">HD Match Streaming</div>
                    <div className="text-[8px] opacity-90">Never Miss a Goal</div>
                  </div>
                  <div className="text-2xl"></div>
                </div>

                <div className="flex items-center gap-1.5 bg-gray-600/30 rounded px-2 py-1 backdrop-blur-sm flex-shrink-0 border border-gray-500/20">
                  <div className="text-white">
                    <div className="text-[9px] font-semibold text-gray-300"> HIGHLIGHTS</div>
                    <div className="text-[10px] font-bold">Match Highlights</div>
                    <div className="text-[8px] opacity-90">Best Moments</div>
                  </div>
                  <div className="text-2xl"></div>
                </div>

                <div className="flex items-center gap-1.5 bg-gray-600/30 rounded px-2 py-1 backdrop-blur-sm flex-shrink-0 border border-gray-500/20">
                  <div className="text-white">
                    <div className="text-[9px] font-semibold text-gray-300"> STATS</div>
                    <div className="text-[10px] font-bold">Live Statistics</div>
                    <div className="text-[8px] opacity-90">Real-time Data</div>
                  </div>
                  <div className="text-2xl"></div>
                </div>

                <div className="flex items-center gap-1.5 bg-gray-600/30 rounded px-2 py-1 backdrop-blur-sm flex-shrink-0 border border-gray-500/20">
                  <div className="text-white">
                    <div className="text-[9px] font-semibold text-gray-300"> ALERTS</div>
                    <div className="text-[10px] font-bold">Goal Notifications</div>
                    <div className="text-[8px] opacity-90">Instant Updates</div>
                  </div>
                  <div className="text-2xl"></div>
                </div>

                <div className="flex items-center gap-1.5 bg-gray-600/30 rounded px-2 py-1 backdrop-blur-sm flex-shrink-0 border border-gray-500/20">
                  <div className="text-white">
                    <div className="text-[9px] font-semibold text-gray-300"> LA LIGA</div>
                    <div className="text-[10px] font-bold">Real Madrid vs Barcelona</div>
                    <div className="text-[8px] opacity-90">El Clasico Tonight</div>
                  </div>
                  <div className="text-2xl"></div>
                </div>

                <div className="flex items-center gap-1.5 bg-gray-600/30 rounded px-2 py-1 backdrop-blur-sm flex-shrink-0 border border-gray-500/20">
                  <div className="text-white">
                    <div className="text-[9px] font-semibold text-gray-300"> PREDICTIONS</div>
                    <div className="text-[10px] font-bold">AI Match Predictions</div>
                    <div className="text-[8px] opacity-90">85% Accuracy Rate</div>
                  </div>
                  <div className="text-2xl"></div>
                </div>
              </div>
            </div>

            {/* Slide 4 - Fantasy & Games */}
            <div className="min-w-full px-4">
              <div className="flex items-center gap-3 overflow-x-auto pb-2">
                <div className="flex items-center gap-1.5 bg-gray-600/30 rounded px-2 py-1 backdrop-blur-sm flex-shrink-0 border border-gray-500/20">
                  <div className="text-white">
                    <div className="text-[9px] font-semibold text-gray-300"> FANTASY</div>
                    <div className="text-[10px] font-bold">Fantasy League</div>
                    <div className="text-[8px] opacity-90">Win ₦1M Weekly</div>
                  </div>
                  <div className="text-2xl"></div>
                </div>

                <div className="flex items-center gap-1.5 bg-gray-600/30 rounded px-2 py-1 backdrop-blur-sm flex-shrink-0 border border-gray-500/20">
                  <div className="text-white">
                    <div className="text-[9px] font-semibold text-gray-300"> MINI GAMES</div>
                    <div className="text-[10px] font-bold">Play & Win</div>
                    <div className="text-[8px] opacity-90">Instant Prizes</div>
                  </div>
                  <div className="text-2xl"></div>
                </div>

                <div className="flex items-center gap-1.5 bg-gray-600/30 rounded px-2 py-1 backdrop-blur-sm flex-shrink-0 border border-gray-500/20">
                  <div className="text-white">
                    <div className="text-[9px] font-semibold text-gray-300"> TOURNAMENTS</div>
                    <div className="text-[10px] font-bold">Weekly Contests</div>
                    <div className="text-[8px] opacity-90">Big Prizes</div>
                  </div>
                  <div className="text-2xl"></div>
                </div>

                <div className="flex items-center gap-1.5 bg-gray-600/30 rounded px-2 py-1 backdrop-blur-sm flex-shrink-0 border border-gray-500/20">
                  <div className="text-white">
                    <div className="text-[9px] font-semibold text-gray-300"> JACKPOT</div>
                    <div className="text-[10px] font-bold">Progressive Jackpot</div>
                    <div className="text-[8px] opacity-90">₦50M+ Prize Pool</div>
                  </div>
                  <div className="text-2xl"></div>
                </div>

                <div className="flex items-center gap-1.5 bg-gray-600/30 rounded px-2 py-1 backdrop-blur-sm flex-shrink-0 border border-gray-500/20">
                  <div className="text-white">
                    <div className="text-[9px] font-semibold text-gray-300"> ESPORTS</div>
                    <div className="text-[10px] font-bold">Esports Betting</div>
                    <div className="text-[8px] opacity-90">FIFA, CS:GO & More</div>
                  </div>
                  <div className="text-2xl"></div>
                </div>
              </div>
            </div>

            {/* Slide 5 - Quick Betting & Features */}
            <div className="min-w-full px-4">
              <div className="flex items-center gap-3 overflow-x-auto pb-2">
                <div className="flex items-center gap-1.5 bg-gray-600/30 rounded px-2 py-1 backdrop-blur-sm flex-shrink-0 border border-gray-500/20">
                  <div className="text-white">
                    <div className="text-[9px] font-semibold text-gray-300"> QUICK BET</div>
                    <div className="text-[10px] font-bold">One-Click Betting</div>
                    <div className="text-[8px] opacity-90">Bet in Seconds</div>
                  </div>
                  <div className="text-2xl"></div>
                </div>

                <div className="flex items-center gap-1.5 bg-gray-600/30 rounded px-2 py-1 backdrop-blur-sm flex-shrink-0 border border-gray-500/20">
                  <div className="text-white">
                    <div className="text-[9px] font-semibold text-gray-300"> CASH OUT</div>
                    <div className="text-[10px] font-bold">Early Cash Out</div>
                    <div className="text-[8px] opacity-90">Secure Your Wins</div>
                  </div>
                  <div className="text-2xl"></div>
                </div>

                <div className="flex items-center gap-1.5 bg-gray-600/30 rounded px-2 py-1 backdrop-blur-sm flex-shrink-0 border border-gray-500/20">
                  <div className="text-white">
                    <div className="text-[9px] font-semibold text-gray-300"> MOBILE APP</div>
                    <div className="text-[10px] font-bold">Download App</div>
                    <div className="text-[8px] opacity-90">Bet Anywhere</div>
                  </div>
                  <div className="text-2xl"></div>
                </div>

                <div className="flex items-center gap-1.5 bg-gray-600/30 rounded px-2 py-1 backdrop-blur-sm flex-shrink-0 border border-gray-500/20">
                  <div className="text-white">
                    <div className="text-[9px] font-semibold text-gray-300"> SECURE</div>
                    <div className="text-[10px] font-bold">Safe & Secure</div>
                    <div className="text-[8px] opacity-90">SSL Protected</div>
                  </div>
                  <div className="text-2xl"></div>
                </div>

                <div className="flex items-center gap-1.5 bg-gray-600/30 rounded px-2 py-1 backdrop-blur-sm flex-shrink-0 border border-gray-500/20">
                  <div className="text-white">
                    <div className="text-[9px] font-semibold text-gray-300"> PAYMENT</div>
                    <div className="text-[10px] font-bold">Instant Deposits</div>
                    <div className="text-[8px] opacity-90">Bank Transfer & Cards</div>
                  </div>
                  <div className="text-2xl"></div>
                </div>
              </div>
            </div>

            {/* Slide 6 - Hot Matches & Promotions */}
            <div className="min-w-full px-4">
              <div className="flex items-center gap-3 overflow-x-auto pb-2">
                <div className="flex items-center gap-1.5 bg-gray-600/30 rounded px-2 py-1 backdrop-blur-sm flex-shrink-0 border border-gray-500/20">
                  <div className="text-white">
                    <div className="text-[9px] font-semibold text-gray-300"> HOT MATCH</div>
                    <div className="text-[10px] font-bold">
                      {matches.length > 0 ? `${matches[0].home_team} vs ${matches[0].away_team}` : 'Big Match Today'}
                    </div>
                    <div className="text-[8px] opacity-90">
                      {matches.length > 0 ? `Best Odds: ${matches[0].home_odds.toFixed(2)}` : "Don't Miss Out!"}
                    </div>
                  </div>
                  <div className="text-2xl"></div>
                </div>

                <div className="flex items-center gap-1.5 bg-gray-600/30 rounded px-2 py-1 backdrop-blur-sm flex-shrink-0 border border-gray-500/20">
                  <div className="text-white">
                    <div className="text-[9px] font-semibold text-gray-300"> BOOST</div>
                    <div className="text-[10px] font-bold">Odds Boost</div>
                    <div className="text-[8px] opacity-90">Enhanced Odds</div>
                  </div>
                  <div className="text-2xl"></div>
                </div>

                <div className="flex items-center gap-1.5 bg-gray-600/30 rounded px-2 py-1 backdrop-blur-sm flex-shrink-0 border border-gray-500/20">
                  <div className="text-white">
                    <div className="text-[9px] font-semibold text-gray-300"> LIMITED</div>
                    <div className="text-[10px] font-bold">Flash Promo</div>
                    <div className="text-[8px] opacity-90">24 Hours Only</div>
                  </div>
                  <div className="text-2xl"></div>
                </div>

                <div className="flex items-center gap-1.5 bg-gray-600/30 rounded px-2 py-1 backdrop-blur-sm flex-shrink-0 border border-gray-500/20">
                  <div className="text-white">
                    <div className="text-[9px] font-semibold text-gray-300"> WEEKEND</div>
                    <div className="text-[10px] font-bold">Weekend Special</div>
                    <div className="text-[8px] opacity-90">Double Rewards</div>
                  </div>
                  <div className="text-2xl"></div>
                </div>

                <div className="flex items-center gap-1.5 bg-gray-600/30 rounded px-2 py-1 backdrop-blur-sm flex-shrink-0 border border-gray-500/20">
                  <div className="text-white">
                    <div className="text-[9px] font-semibold text-gray-300"> LEAGUES</div>
                    <div className="text-[10px] font-bold">All Major Leagues</div>
                    <div className="text-[8px] opacity-90">EPL, La Liga, Serie A</div>
                  </div>
                  <div className="text-2xl"></div>
                </div>
              </div>
            </div>
          </div>
          
          {/* Slide indicators */}
          <div className="absolute bottom-1 left-1/2 transform -translate-x-1/2 flex gap-1">
            {[0, 1, 2, 3, 4, 5].map((index) => (
              <button
                key={index}
                onClick={() => setCurrentAdIndex(index)}
                className={`w-1.5 h-1.5 rounded-full transition-all ${
                  currentAdIndex === index ? 'bg-white' : 'bg-white/40'
                }`}
              />
            ))}
          </div>
        </div>
      </div>

        {/* Main Content */}
        <main className="w-full max-w-full mx-auto px-2 sm:px-4 lg:px-6 py-2 pb-20 relative z-10 flex-1 overflow-y-auto overflow-x-hidden">
        
        {/* Error Message */}
        {error && (
          <div className="mb-4 bg-danger/20 border border-danger rounded-card p-3">
            <div className="flex items-start gap-2">
              <div className="text-danger text-lg">⚠</div>
              <div className="flex-1">
                <h3 className="text-danger text-xs font-semibold mb-1">Error Loading Data</h3>
                <p className="text-danger/90 text-[10px] mb-2">{error}</p>
                <button
                  onClick={() => loadData()}
                  className="px-3 py-1 bg-danger hover:bg-danger/90 text-white rounded-lg font-semibold text-[10px] transition-all"
                >
                  Retry
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Matches - Responsive Layout */}
        {showMatches && (
          <>
            {/* Desktop: Table View (hidden on mobile) */}
            <div className="hidden md:block">
              <MatchTable
                matches={filteredMatches}
                selectedDate={selectedDate}
                loading={matchesLoading}
                onBetClick={handleBetClick}
              />
            </div>

            {/* Mobile: Card View (hidden on desktop) */}
            <div className="block md:hidden">
              <MatchCardList
                matches={filteredMatches}
                selectedDate={selectedDate}
                loading={matchesLoading}
                onBetClick={handleBetClick}
              />
            </div>
          </>
        )}
        </main>

        {/* Betting Modal */}
        <BettingModal
          isOpen={bettingModalOpen}
          onClose={() => setBettingModalOpen(false)}
          match={selectedMatch}
          selectedBetType={selectedBetType}
          walletBalance={wallet?.balance || 0}
          onPlaceBet={handlePlaceSingleBet}
          onTopUp={handleTopUp}
        />

        {/* Betslip Widget */}
        <BetslipWidget
          selections={betSelections}
          onRemove={handleRemoveSelection}
          onClear={handleClearBetslip}
          onPlaceBet={handlePlaceBet}
          walletBalance={wallet?.balance || 0}
        />
      </div>

      {/* Quick Access Sidebar */}
        {bottomMenuOpen && activeBottomTab === 'quick-access' && (
          <div className="fixed inset-0 z-50 flex">
            {/* Sidebar */}
            <div className="w-80 bg-gradient-to-b from-gray-900 via-gray-800 to-gray-900 border-r border-gray-600 shadow-2xl overflow-y-auto transform transition-transform duration-300 ease-out">
              <div className="p-6">
                {/* Sidebar Header */}
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <h2 className="text-[10px] font-bold text-white mb-1">Quick Access</h2>
                    <div className="w-8 h-0.5 bg-gradient-to-r from-gray-400 to-gray-600 rounded-full"></div>
                  </div>
                  <button
                    onClick={() => setBottomMenuOpen(false)}
                    className="p-1.5 hover:bg-gray-700 rounded-lg transition-all"
                  >
                    <span className="text-gray-400 hover:text-white text-sm"></span>
                  </button>
                </div>

                {/* Main Navigation */}
                <div className="mb-4">
                  <div className="space-y-1">
                    <Link href="/dashboard" className="flex items-center gap-2 px-3 py-2 rounded-lg bg-gray-600/20 text-gray-300 text-xs font-semibold transition-all hover:bg-gray-600/30">
                      <span className="text-sm"></span>
                      <span>Live Matches</span>
                    </Link>
                    <Link href="/fantasy" className="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-gray-700 text-gray-300 hover:text-white text-xs transition-all">
                      <span className="text-sm"></span>
                      <span>Fantasy League</span>
                    </Link>
                    <Link href="/bets" className="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-gray-700 text-gray-300 hover:text-white text-xs transition-all">
                      <span className="text-sm"></span>
                      <span>My Bets</span>
                    </Link>
                    <Link href="/wallet" className="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-gray-700 text-gray-300 hover:text-white transition-all">
                      <span className="text-xl"></span>
                      <span>Wallet</span>
                    </Link>
                    <Link href="/profile" className="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-gray-700 text-gray-300 hover:text-white transition-all">
                      <span className="text-xl"></span>
                      <span>Profile</span>
                    </Link>
                  </div>
                </div>

                {/* Today's Matches Info */}
                <div className="mb-6 bg-gradient-to-r from-primary/10 to-cyan/10 rounded-lg p-4 border border-primary/20">
                  <div className="text-sm text-gray-400 mb-2">Today's Matches</div>
                  <div className="text-2xl font-bold text-primary">{matches.length}</div>
                  <div className="text-xs text-gray-400">Live & Upcoming</div>
                </div>

                {/* Additional Quick Actions */}
                <div>
                  <h4 className="text-white font-semibold text-sm mb-3">More Options</h4>
                  <div className="grid grid-cols-3 gap-3">
                    <Link href="/live" className="bg-gradient-to-r from-red-600 to-red-700 hover:from-red-500 hover:to-red-600 p-3 rounded-lg text-center transition-all transform hover:scale-105">
                      <div className="text-xl mb-1"></div>
                      <div className="text-white font-semibold text-xs">Live</div>
                    </Link>
                    <Link href="/popular" className="bg-gradient-to-r from-orange-600 to-orange-700 hover:from-orange-500 hover:to-orange-600 p-3 rounded-lg text-center transition-all transform hover:scale-105">
                      <div className="text-xl mb-1"></div>
                      <div className="text-white font-semibold text-xs">Popular</div>
                    </Link>
                    <Link href="/promotions" className="bg-gradient-to-r from-green-600 to-green-700 hover:from-green-500 hover:to-green-600 p-3 rounded-lg text-center transition-all transform hover:scale-105">
                      <div className="text-xl mb-1"></div>
                      <div className="text-white font-semibold text-xs">Promos</div>
                    </Link>
                  </div>
                </div>
              </div>
            </div>
            
            {/* Invisible overlay for closing */}
            <div 
              className="flex-1"
              onClick={() => setBottomMenuOpen(false)}
            ></div>
          </div>
        )}

        {/* Bottom Navigation Menu */}
        <div className="fixed bottom-0 left-0 right-0 z-50">
          {/* Betslip and My Bets Panel */}
          {bottomMenuOpen && (activeBottomTab === 'betslip' || activeBottomTab === 'my-bets') && (
            <div className="bg-gradient-to-t from-gray-900 via-gray-800 to-gray-900 border-t border-gray-600 shadow-2xl w-full">
              <div className="w-full mx-auto">
                {/* Tab Navigation */}
                <div className="flex border-b border-gray-600">
                  <button
                    onClick={() => setActiveBottomTab('betslip')}
                    className={`flex-1 px-4 py-3 text-sm font-semibold transition-all relative ${
                      activeBottomTab === 'betslip'
                        ? 'bg-primary text-white border-b-2 border-primary'
                        : 'text-gray-300 hover:text-white hover:bg-gray-700'
                    }`}
                  >
                     Betslip
                    {betslipItems.length > 0 && (
                      <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                        {betslipItems.length}
                      </span>
                    )}
                  </button>
                  <button
                    onClick={() => setActiveBottomTab('my-bets')}
                    className={`flex-1 px-4 py-3 text-sm font-semibold transition-all relative ${
                      activeBottomTab === 'my-bets'
                        ? 'bg-primary text-white border-b-2 border-primary'
                        : 'text-gray-300 hover:text-white hover:bg-gray-700'
                    }`}
                  >
                     My Bets
                    {myBets.length > 0 && (
                      <span className="absolute -top-1 -right-1 bg-green-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                        {myBets.length}
                      </span>
                    )}
                  </button>
                </div>

                {/* Tab Content */}
                <div className="p-4 max-h-80 overflow-y-auto">
                  {/* Betslip Tab */}
                  {activeBottomTab === 'betslip' && (
                    <div className="space-y-6">
                      {betslipItems.length === 0 ? (
                        <div>
                          {/* Empty Betslip State */}
                          <div className="text-center py-6">
                            <div className="text-4xl mb-3"></div>
                            <h3 className="text-white font-bold text-base mb-2">Betslip is empty.</h3>
                            <p className="text-gray-400 text-xs mb-4">Check out some of our recommended events below.</p>
                          </div>

                          {/* Load Booking Code Section */}
                          <div className="mb-4">
                            <p className="text-gray-300 text-xs mb-2">Enter a Booking Number below and the selection will be added to your betslip.</p>
                            <div className="mb-1">
                              <label className="text-white text-xs font-semibold">Load Booking Code:</label>
                            </div>
                            <div className="flex gap-2">
                              <input
                                type="text"
                                placeholder="Enter booking code..."
                                className="flex-1 px-3 py-2 bg-gray-700 border border-gray-600 rounded text-white text-xs focus:border-primary focus:outline-none"
                              />
                              <button className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded text-xs font-semibold transition-all">
                                Book
                              </button>
                            </div>
                          </div>

                          {/* Recommended Events */}
                          <div>
                            <h4 className="text-white font-semibold text-sm mb-3">Recommended Events</h4>
                            <div className="space-y-2">
                              {/* Sample Recommended Events */}
                              <div className="bg-gray-800 rounded p-3 border border-gray-600 hover:border-primary/50 transition-all cursor-pointer">
                                <div className="flex justify-between items-center mb-1">
                                  <div>
                                    <div className="text-white font-semibold text-xs">Manchester United vs Arsenal</div>
                                    <div className="text-gray-400 text-xs">Premier League • Today 3:00 PM</div>
                                  </div>
                                  <div className="text-primary font-bold text-sm">2.15</div>
                                </div>
                                <div className="text-gray-300 text-xs">Manchester United Win</div>
                              </div>

                              <div className="bg-gray-800 rounded p-3 border border-gray-600 hover:border-primary/50 transition-all cursor-pointer">
                                <div className="flex justify-between items-center mb-1">
                                  <div>
                                    <div className="text-white font-semibold text-xs">Barcelona vs Real Madrid</div>
                                    <div className="text-gray-400 text-xs">La Liga • Tomorrow 8:00 PM</div>
                                  </div>
                                  <div className="text-primary font-bold text-sm">1.95</div>
                                </div>
                                <div className="text-gray-300 text-xs">Over 2.5 Goals</div>
                              </div>

                              <div className="bg-gray-800 rounded p-3 border border-gray-600 hover:border-primary/50 transition-all cursor-pointer">
                                <div className="flex justify-between items-center mb-1">
                                  <div>
                                    <div className="text-white font-semibold text-xs">Chelsea vs Liverpool</div>
                                    <div className="text-gray-400 text-xs">Premier League • Sunday 4:30 PM</div>
                                  </div>
                                  <div className="text-primary font-bold text-sm">3.20</div>
                                </div>
                                <div className="text-gray-300 text-xs">Both Teams to Score</div>
                              </div>

                              <div className="bg-gray-800 rounded p-3 border border-gray-600 hover:border-primary/50 transition-all cursor-pointer">
                                <div className="flex justify-between items-center mb-1">
                                  <div>
                                    <div className="text-white font-semibold text-xs">Bayern Munich vs Dortmund</div>
                                    <div className="text-gray-400 text-xs">Bundesliga • Saturday 2:30 PM</div>
                                  </div>
                                  <div className="text-primary font-bold text-sm">1.75</div>
                                </div>
                                <div className="text-gray-300 text-xs">Bayern Munich Win</div>
                              </div>
                            </div>
                          </div>
                        </div>
                      ) : (
                        <div className="space-y-4">
                          {/* Active Betslip */}
                          <div className="space-y-3">
                            {betslipItems.map((item, index) => (
                              <div key={index} className="bg-gray-800 rounded-lg p-4 border border-gray-600">
                                <div className="flex justify-between items-start mb-2">
                                  <div>
                                    <div className="text-white font-semibold text-sm">{item.match}</div>
                                    <div className="text-gray-400 text-xs">{item.selection}</div>
                                  </div>
                                  <div className="text-primary font-bold">{item.odds}</div>
                                </div>
                                <div className="flex gap-2">
                                  <input
                                    type="number"
                                    placeholder="Stake"
                                    className="flex-1 px-3 py-2 bg-gray-700 border border-gray-600 rounded text-white text-sm focus:border-primary focus:outline-none"
                                  />
                                  <button className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded text-sm transition-all">
                                    Remove
                                  </button>
                                </div>
                              </div>
                            ))}
                          </div>

                          {/* Betslip Summary */}
                          <div className="bg-primary/20 rounded p-3 border border-primary/30">
                            <div className="flex justify-between items-center mb-2">
                              <span className="text-white font-semibold text-xs">Total Stake:</span>
                              <span className="text-white font-bold text-xs">₦0.00</span>
                            </div>
                            <div className="flex justify-between items-center mb-3">
                              <span className="text-white font-semibold text-xs">Potential Win:</span>
                              <span className="text-primary font-bold text-sm">₦0.00</span>
                            </div>
                            <button className="w-full py-2 bg-primary hover:bg-primary/90 text-white rounded text-xs font-bold transition-all">
                              Place Bet
                            </button>
                          </div>

                          {/* Load Booking Code (also available when betslip has items) */}
                          <div className="border-t border-gray-600 pt-3">
                            <div className="mb-1">
                              <label className="text-white text-xs font-semibold">Load Booking Code:</label>
                            </div>
                            <div className="flex gap-2">
                              <input
                                type="text"
                                placeholder="Enter booking code..."
                                className="flex-1 px-3 py-2 bg-gray-700 border border-gray-600 rounded text-white text-xs focus:border-primary focus:outline-none"
                              />
                              <button className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded text-xs font-semibold transition-all">
                                Book
                              </button>
                            </div>
                          </div>
                        </div>
                      )}
                    </div>
                  )}

                  {/* My Bets Tab */}
                  {activeBottomTab === 'my-bets' && (
                    <div>
                      {myBets.length === 0 ? (
                        <div className="text-center py-8">
                          <div className="text-6xl mb-4"></div>
                          <h3 className="text-white font-semibold mb-2">No Active Bets</h3>
                          <p className="text-gray-400 text-sm mb-4">Your active and recent bets will appear here</p>
                          <div className="flex gap-3 justify-center">
                            <Link href="/bets" className="px-6 py-2 bg-primary hover:bg-primary/90 text-white rounded-lg font-semibold transition-all">
                              View All Bets
                            </Link>
                            <button
                              onClick={() => setBottomMenuOpen(false)}
                              className="px-6 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg font-semibold transition-all"
                            >
                              Place New Bet
                            </button>
                          </div>
                        </div>
                      ) : (
                        <div className="space-y-3">
                          {myBets.map((bet, index) => (
                            <div key={index} className="bg-gray-800 rounded-lg p-4 border border-gray-600">
                              <div className="flex justify-between items-start mb-2">
                                <div>
                                  <div className="text-white font-semibold text-sm">{bet.match}</div>
                                  <div className="text-gray-400 text-xs">{bet.selection} • Stake: ₦{bet.stake}</div>
                                </div>
                                <div className={`px-2 py-1 rounded text-xs font-semibold ${
                                  bet.status === 'won' ? 'bg-green-600 text-white' :
                                  bet.status === 'lost' ? 'bg-red-600 text-white' :
                                  'bg-yellow-600 text-white'
                                }`}>
                                  {bet.status.toUpperCase()}
                                </div>
                              </div>
                              <div className="flex justify-between items-center">
                                <span className="text-gray-400 text-xs">Potential Win: ₦{bet.potentialWin}</span>
                                <span className="text-primary font-bold">{bet.odds}</span>
                              </div>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Bottom Menu Trigger */}
          <div className="bg-gradient-to-r from-gray-900 via-black to-gray-900 border-t border-white/10 w-full">
            <div className="w-full mx-auto px-4 py-2">
              <div className="flex items-center justify-between">
                {/* A-Z Menu Button */}
                <button
                  onClick={() => {
                    setActiveBottomTab('quick-access');
                    setBottomMenuOpen(!bottomMenuOpen);
                  }}
                  className="flex items-center gap-1.5 px-3 py-1.5 bg-black/60 hover:bg-black/70 backdrop-blur-sm text-white rounded-lg font-semibold transition-all transform hover:scale-105 shadow-lg border border-white/20"
                >
                  <span className="text-sm"></span>
                  <span className="text-xs" style={{ textShadow: '0 4px 6px rgba(0, 0, 139, 0.8), 0 2px 4px rgba(0, 0, 139, 0.6)' }}>A-Z Menu</span>
                  <span className={`transform transition-transform text-xs ${bottomMenuOpen && activeBottomTab === 'quick-access' ? 'rotate-180' : ''}`}>
                    
                  </span>
                </button>

                {/* Center Betslip Button */}
                <button
                  onClick={() => {
                    setActiveBottomTab('betslip');
                    setBottomMenuOpen(true);
                  }}
                  className="relative px-4 py-2 bg-black/60 hover:bg-black/70 backdrop-blur-sm text-white rounded-lg font-semibold transition-all transform hover:scale-105 shadow-lg border border-white/20"
                >
                  <span className="text-base mr-1.5"></span>
                  <span className="text-xs" style={{ textShadow: '0 4px 6px rgba(0, 0, 139, 0.8), 0 2px 4px rgba(0, 0, 139, 0.6)' }}>Betslip</span>
                  {betslipItems.length > 0 && (
                    <span className="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center font-bold shadow-lg">
                      {betslipItems.length}
                    </span>
                  )}
                </button>

                {/* My Bets Button */}
                <button
                  onClick={() => {
                    setActiveBottomTab('my-bets');
                    setBottomMenuOpen(true);
                  }}
                  className="relative flex items-center gap-1.5 px-3 py-1.5 bg-black/60 hover:bg-black/70 backdrop-blur-sm text-white rounded-lg font-semibold transition-all transform hover:scale-105 shadow-lg border border-white/20"
                >
                  <span className="text-sm"></span>
                  <span className="text-xs" style={{ textShadow: '0 4px 6px rgba(0, 0, 139, 0.8), 0 2px 4px rgba(0, 0, 139, 0.6)' }}>My Bets</span>
                  {myBets.length > 0 && (
                    <span className="absolute -top-1 -right-1 bg-green-500 text-white text-xs rounded-full w-4 h-4 flex items-center justify-center shadow-lg">
                      {myBets.length}
                    </span>
                  )}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
  );
}