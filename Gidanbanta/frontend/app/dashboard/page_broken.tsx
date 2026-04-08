'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuth } from '@/contexts/AuthContext';
import { api } from '@/lib/api';
import dynamic from 'next/dynamic';
import DateSelector from '@/components/DateSelector';
import LeagueFilter from '@/components/LeagueFilter';
import MatchTable from '@/components/MatchTable';
import MatchCardList from '@/components/MatchCardList';
import AccountDropdown from '@/components/AccountDropdown';

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

export default function DashboardPage() {
  const { user, loading: authLoading, logout } = useAuth();
  const router = useRouter();
  const [matches, setMatches] = useState<CalendarMatch[]>([]);
  const [wallet, setWallet] = useState<Wallet | null>(null);
  const [leagues, setLeagues] = useState<League[]>([]);
  const [selectedDate, setSelectedDate] = useState<string>(new Date().toISOString().split('T')[0]);
  const [selectedLeague, setSelectedLeague] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');
  const [bettingModalOpen, setBettingModalOpen] = useState(false);
  const [selectedMatch, setSelectedMatch] = useState<CalendarMatch | null>(null);
  const [selectedBetType, setSelectedBetType] = useState<'home' | 'draw' | 'away'>('home');
  const [currentAdIndex, setCurrentAdIndex] = useState(0);
  const [bottomMenuOpen, setBottomMenuOpen] = useState(false);
  const [activeBottomTab, setActiveBottomTab] = useState<'quick-access' | 'betslip' | 'my-bets'>('quick-access');
  const [betslipItems, setBetslipItems] = useState<any[]>([]);
  const [myBets, setMyBets] = useState<any[]>([]);

  useEffect(() => {
    if (!authLoading && !user) {
      router.push('/login');
    } else if (user) {
      loadData();
    }
  }, [user, authLoading]);

  useEffect(() => {
    if (user && selectedDate) {
      loadMatches();
    }
  }, [selectedDate, selectedLeague]);

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
      // Load wallet
      const walletResponse = await api.getWallet();
      if (walletResponse.data) {
        setWallet(walletResponse.data as Wallet);
      }

      // Load matches for today
      await loadMatches();
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
      setError('');
      
      // Load matches
      const matchesResponse = await api.getCalendarMatches({
        start_date: today,
        end_date: endDate,
        league_id: selectedLeague || undefined
      });

      if (matchesResponse.data) {
        const data = matchesResponse.data as any;
        setMatches(data.matches || []);
      }

      // Load leagues
      if (!selectedLeague) {
        const leaguesResponse = await api.getAvailableLeagues(today, endDate);
        if (leaguesResponse.data) {
          setLeagues(leaguesResponse.data as League[]);
        }
      }
    } catch (err: any) {
      console.error('Error loading matches:', err);
      setError(err.message || 'Failed to load matches. Please try again.');
      // Keep existing matches on error
    }
  };

  const handleBetClick = (match: CalendarMatch, betType: 'home' | 'draw' | 'away') => {
    setSelectedMatch(match);
    setSelectedBetType(betType);
    setBettingModalOpen(true);
  };

  const handlePlaceBet = async (matchId: number, betType: 'home' | 'draw' | 'away', stake: number) => {
    // TODO: Implement actual bet placement API call
    console.log('Placing bet:', { matchId, betType, stake });
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
    <div className="min-h-screen bg-navy relative overflow-hidden">
      {/* Main Content Area - Full Screen */}
      <div className="relative overflow-hidden">
        {/* Animated Football Background */}
        <div className="fixed inset-0 z-0 opacity-5">
          <div 
            className="absolute inset-0 bg-cover bg-center animate-pulse"
            style={{
              backgroundImage: "url('https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=1920&q=80')",
              animation: "float 20s ease-in-out infinite"
            }}
          ></div>
        </div>
        
        {/* Floating football icons animation */}
        <div className="fixed inset-0 z-0 pointer-events-none">
          <div className="absolute top-20 left-10 text-6xl opacity-10 animate-bounce" style={{ animationDelay: '0s', animationDuration: '3s' }}>⚽</div>
          <div className="absolute top-40 right-20 text-5xl opacity-10 animate-bounce" style={{ animationDelay: '1s', animationDuration: '4s' }}>⚽</div>
          <div className="absolute bottom-32 left-1/4 text-7xl opacity-10 animate-bounce" style={{ animationDelay: '2s', animationDuration: '5s' }}>⚽</div>
          <div className="absolute bottom-20 right-1/3 text-6xl opacity-10 animate-bounce" style={{ animationDelay: '1.5s', animationDuration: '3.5s' }}>⚽</div>
        </div>

      {/* Header - Dark Shining 3D Style */}
      <header className="bg-gradient-to-br from-gray-900 via-gray-800 to-black shadow-2xl relative z-10 border-b border-gray-700" 
              style={{
                background: 'linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 25%, #1a1a1a 50%, #0f0f0f 75%, #000000 100%)',
                boxShadow: 'inset 0 1px 0 rgba(255,255,255,0.1), 0 10px 30px rgba(0,0,0,0.5)',
              }}>
        {/* Top Bar - Logo, Amount, Account */}
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            {/* Left - GidanBanta Logo */}
            <div className="flex-1">
              <h1 className="text-4xl font-heading font-bold italic bg-gradient-to-r from-cyan via-yellow-400 to-green-400 bg-clip-text text-transparent drop-shadow-lg">
                GidanBanta
              </h1>
            </div>

            {/* Right - Wallet & Account */}
            <div className="flex items-center gap-4">
              {/* Wallet Balance */}
              <Link href="/wallet" className="bg-gradient-to-br from-gray-700 to-gray-900 hover:from-gray-600 hover:to-gray-800 backdrop-blur-sm px-4 py-3 rounded-lg border border-gray-600 shadow-lg transition-all transform hover:scale-105"
                    style={{
                      boxShadow: 'inset 0 1px 0 rgba(255,255,255,0.1), 0 4px 15px rgba(0,0,0,0.3)',
                    }}>
                <div className="flex items-center gap-3">
                  <div className="text-white">
                    <div className="text-xl font-bold">
                      ₦{wallet?.balance.toFixed(2) || '0.00'}
                    </div>
                  </div>
                  <div className="text-2xl">💰</div>
                </div>
              </Link>

              {/* Account Dropdown */}
              <AccountDropdown user={user} onLogout={logout} onTopUp={handleTopUp} />
            </div>
          </div>
        </div>

        {/* Navigation Bar */}
        <div className="border-t border-gray-600" 
             style={{
               background: 'linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 50%, #0a0a0a 100%)',
               boxShadow: 'inset 0 1px 0 rgba(255,255,255,0.05)',
             }}>
          <div className="max-w-7xl mx-auto px-6 py-3">
            <div className="flex flex-col items-center gap-3">
              {/* Main Navigation */}
              <nav className="flex items-center gap-1 bg-gradient-to-r from-gray-800 to-gray-900 backdrop-blur-sm rounded-lg p-1 border border-gray-600 shadow-lg"
                   style={{
                     boxShadow: 'inset 0 1px 0 rgba(255,255,255,0.1), 0 4px 15px rgba(0,0,0,0.3)',
                   }}>
                <Link href="/dashboard" className="px-6 py-2 bg-gradient-to-r from-gray-600 to-gray-700 text-white font-semibold rounded-md transition-all hover:from-gray-500 hover:to-gray-600 shadow-md transform hover:scale-105">
                  Matches
                </Link>
                <Link href="/fantasy" className="px-6 py-2 text-white/80 hover:text-white hover:bg-gradient-to-r hover:from-gray-700 hover:to-gray-800 rounded-md transition-all">
                  Fantasy
                </Link>
              </nav>

              {/* League Navigation */}
              <nav className="flex items-center gap-1 bg-gradient-to-r from-gray-900 to-black backdrop-blur-sm rounded-lg p-1 border border-gray-700 overflow-x-auto max-w-full shadow-lg"
                   style={{
                     boxShadow: 'inset 0 1px 0 rgba(255,255,255,0.05), 0 4px 15px rgba(0,0,0,0.4)',
                   }}>
                <button 
                  onClick={() => setSelectedLeague(null)}
                  className={`px-4 py-2 text-sm font-medium rounded-md transition-all whitespace-nowrap transform hover:scale-105 ${
                    selectedLeague === null 
                      ? 'bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-lg' 
                      : 'text-gray-300 hover:bg-gradient-to-r hover:from-gray-700 hover:to-gray-800 hover:text-white'
                  }`}
                  style={selectedLeague === null ? {
                    boxShadow: 'inset 0 1px 0 rgba(255,255,255,0.2), 0 4px 15px rgba(59, 130, 246, 0.3)',
                  } : {}}
                >
                  All Leagues
                </button>
                {leagues.slice(0, 8).map((league) => (
                  <button
                    key={league.id}
                    onClick={() => setSelectedLeague(league.id)}
                    className={`px-4 py-2 text-sm font-medium rounded-md transition-all whitespace-nowrap transform hover:scale-105 ${
                      selectedLeague === league.id
                        ? 'bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-lg'
                        : 'text-gray-300 hover:bg-gradient-to-r hover:from-gray-700 hover:to-gray-800 hover:text-white'
                    }`}
                    style={selectedLeague === league.id ? {
                      boxShadow: 'inset 0 1px 0 rgba(255,255,255,0.2), 0 4px 15px rgba(59, 130, 246, 0.3)',
                    } : {}}
                  >
                    {league.name}
                  </button>
                ))}
                {leagues.length > 8 && (
                  <button className="px-4 py-2 text-sm font-medium text-gray-400 hover:bg-gradient-to-r hover:from-gray-700 hover:to-gray-800 hover:text-white rounded-md transition-all transform hover:scale-105">
                    +{leagues.length - 8} More
                  </button>
                )}
              </nav>
            </div>
          </div>
        </div>
      </header>

      {/* Advertisement Banner */}
      <div className="bg-gradient-to-r from-green-600 via-green-700 to-green-800 border-b border-green-500 relative z-10 overflow-hidden">
        <div className="relative h-20 flex items-center">
          <div 
            className="flex transition-transform duration-500 ease-in-out" 
            style={{ transform: `translateX(-${currentAdIndex * 100}%)` }}
          >
            {/* Slide 1 - Welcome & Bonus Ads */}
            <div className="min-w-full px-4">
              <div className="flex items-center gap-3 overflow-x-auto pb-2">
                <div className="flex items-center gap-2 bg-yellow-500/30 rounded-lg px-4 py-2 backdrop-blur-sm flex-shrink-0 border border-yellow-400/20">
                  <div className="text-white">
                    <div className="text-xs font-semibold text-yellow-300">💰 WELCOME BONUS</div>
                    <div className="text-sm font-bold">100% First Deposit</div>
                    <div className="text-xs opacity-90">Up to ₦20,000</div>
                  </div>
                  <div className="text-2xl">🎁</div>
                </div>
                
                <div className="flex items-center gap-2 bg-green-500/30 rounded-lg px-4 py-2 backdrop-blur-sm flex-shrink-0 border border-green-400/20">
                  <div className="text-white">
                    <div className="text-xs font-semibold text-green-300">🎯 CASHBACK</div>
                    <div className="text-sm font-bold">10% Weekly Cashback</div>
                    <div className="text-xs opacity-90">Every Monday</div>
                  </div>
                  <div className="text-2xl">💸</div>
                </div>

                <div className="flex items-center gap-2 bg-purple-500/30 rounded-lg px-4 py-2 backdrop-blur-sm flex-shrink-0 border border-purple-400/20">
                  <div className="text-white">
                    <div className="text-xs font-semibold text-purple-300">🏆 VIP CLUB</div>
                    <div className="text-sm font-bold">Join VIP Program</div>
                    <div className="text-xs opacity-90">Exclusive Rewards</div>
                  </div>
                  <div className="text-2xl">👑</div>
                </div>

                <div className="flex items-center gap-2 bg-blue-500/30 rounded-lg px-4 py-2 backdrop-blur-sm flex-shrink-0 border border-blue-400/20">
                  <div className="text-white">
                    <div className="text-xs font-semibold text-blue-300">🎲 CASINO</div>
                    <div className="text-sm font-bold">Live Casino Games</div>
                    <div className="text-xs opacity-90">Real Dealers 24/7</div>
                  </div>
                  <div className="text-2xl">🎰</div>
                </div>

                <div className="flex items-center gap-2 bg-emerald-500/30 rounded-lg px-4 py-2 backdrop-blur-sm flex-shrink-0 border border-emerald-400/20">
                  <div className="text-white">
                    <div className="text-xs font-semibold text-emerald-300">⚽ LIVE MATCH</div>
                    <div className="text-sm font-bold">Chelsea vs Arsenal</div>
                    <div className="text-xs opacity-90">Odds: 2.15 vs 1.95</div>
                  </div>
                  <div className="text-2xl">🔥</div>
                </div>

                <div className="flex items-center gap-2 bg-red-500/30 rounded-lg px-4 py-2 backdrop-blur-sm flex-shrink-0 border border-red-400/20">
                  <div className="text-white">
                    <div className="text-xs font-semibold text-red-300">🎯 ACCA BOOST</div>
                    <div className="text-sm font-bold">Accumulator Boost</div>
                    <div className="text-xs opacity-90">Up to 70% Extra</div>
                  </div>
                  <div className="text-2xl">🚀</div>
                </div>
              </div>
            </div>

            {/* Slide 2 - Banta Room & Social Ads */}
            <div className="min-w-full px-4">
              <div className="flex items-center gap-3 overflow-x-auto pb-2">
                <div className="flex items-center gap-2 bg-blue-500/30 rounded-lg px-4 py-2 backdrop-blur-sm flex-shrink-0 border border-blue-400/20">
                  <div className="text-white">
                    <div className="text-xs font-semibold text-blue-300">🏠 BANTA ROOM</div>
                    <div className="text-sm font-bold">Visit Your Room</div>
                    <div className="text-xs opacity-90">Private Chat & Rewards</div>
                  </div>
                  <div className="text-2xl">🏠</div>
                </div>

                <div className="flex items-center gap-2 bg-pink-500/30 rounded-lg px-4 py-2 backdrop-blur-sm flex-shrink-0 border border-pink-400/20">
                  <div className="text-white">
                    <div className="text-xs font-semibold text-pink-300">💬 COMMUNITY</div>
                    <div className="text-sm font-bold">Join Chat Groups</div>
                    <div className="text-xs opacity-90">Connect with Fans</div>
                  </div>
                  <div className="text-2xl">👥</div>
                </div>

                <div className="flex items-center gap-2 bg-indigo-500/30 rounded-lg px-4 py-2 backdrop-blur-sm flex-shrink-0 border border-indigo-400/20">
                  <div className="text-white">
                    <div className="text-xs font-semibold text-indigo-300">🎖️ LEADERBOARD</div>
                    <div className="text-sm font-bold">Top Winners</div>
                    <div className="text-xs opacity-90">Weekly Rankings</div>
                  </div>
                  <div className="text-2xl">🏅</div>
                </div>

                <div className="flex items-center gap-2 bg-teal-500/30 rounded-lg px-4 py-2 backdrop-blur-sm flex-shrink-0 border border-teal-400/20">
                  <div className="text-white">
                    <div className="text-xs font-semibold text-teal-300">🎁 DAILY BONUS</div>
                    <div className="text-sm font-bold">Login Rewards</div>
                    <div className="text-xs opacity-90">Claim Daily</div>
                  </div>
                  <div className="text-2xl">📅</div>
                </div>

                <div className="flex items-center gap-2 bg-slate-500/30 rounded-lg px-4 py-2 backdrop-blur-sm flex-shrink-0 border border-slate-400/20">
                  <div className="text-white">
                    <div className="text-xs font-semibold text-slate-300">⚽ PREMIER LEAGUE</div>
                    <div className="text-sm font-bold">Man City vs Liverpool</div>
                    <div className="text-xs opacity-90">Today 3:00 PM</div>
                  </div>
                  <div className="text-2xl">🏆</div>
                </div>

                <div className="flex items-center gap-2 bg-orange-500/30 rounded-lg px-4 py-2 backdrop-blur-sm flex-shrink-0 border border-orange-400/20">
                  <div className="text-white">
                    <div className="text-xs font-semibold text-orange-300">🏃 LIVE BETTING</div>
                    <div className="text-sm font-bold">In-Play Betting</div>
                    <div className="text-xs opacity-90">Bet While Watching</div>
                  </div>
                  <div className="text-2xl">⚽</div>
                </div>
              </div>
            </div>

            {/* Slide 3 - Live Streaming & Entertainment */}
            <div className="min-w-full px-4">
              <div className="flex items-center gap-3 overflow-x-auto pb-2">
                <div className="flex items-center gap-2 bg-red-500/30 rounded-lg px-4 py-2 backdrop-blur-sm flex-shrink-0 border border-red-400/20">
                  <div className="text-white">
                    <div className="text-xs font-semibold text-red-300">📺 LIVE STREAM</div>
                    <div className="text-sm font-bold">HD Match Streaming</div>
                    <div className="text-xs opacity-90">Never Miss a Goal</div>
                  </div>
                  <div className="text-2xl">📱</div>
                </div>

                <div className="flex items-center gap-2 bg-orange-500/30 rounded-lg px-4 py-2 backdrop-blur-sm flex-shrink-0 border border-orange-400/20">
                  <div className="text-white">
                    <div className="text-xs font-semibold text-orange-300">🎬 HIGHLIGHTS</div>
                    <div className="text-sm font-bold">Match Highlights</div>
                    <div className="text-xs opacity-90">Best Moments</div>
                  </div>
                  <div className="text-2xl">⚡</div>
                </div>

                <div className="flex items-center gap-2 bg-cyan-500/30 rounded-lg px-4 py-2 backdrop-blur-sm flex-shrink-0 border border-cyan-400/20">
                  <div className="text-white">
                    <div className="text-xs font-semibold text-cyan-300">📊 STATS</div>
                    <div className="text-sm font-bold">Live Statistics</div>
                    <div className="text-xs opacity-90">Real-time Data</div>
                  </div>
                  <div className="text-2xl">📈</div>
                </div>

                <div className="flex items-center gap-2 bg-lime-500/30 rounded-lg px-4 py-2 backdrop-blur-sm flex-shrink-0 border border-lime-400/20">
                  <div className="text-white">
                    <div className="text-xs font-semibold text-lime-300">🔔 ALERTS</div>
                    <div className="text-sm font-bold">Goal Notifications</div>
                    <div className="text-xs opacity-90">Instant Updates</div>
                  </div>
                  <div className="text-2xl">🚨</div>
                </div>

                <div className="flex items-center gap-2 bg-stone-500/30 rounded-lg px-4 py-2 backdrop-blur-sm flex-shrink-0 border border-stone-400/20">
                  <div className="text-white">
                    <div className="text-xs font-semibold text-stone-300">⚽ LA LIGA</div>
                    <div className="text-sm font-bold">Real Madrid vs Barcelona</div>
                    <div className="text-xs opacity-90">El Clasico Tonight</div>
                  </div>
                  <div className="text-2xl">🔥</div>
                </div>

                <div className="flex items-center gap-2 bg-emerald-500/30 rounded-lg px-4 py-2 backdrop-blur-sm flex-shrink-0 border border-emerald-400/20">
                  <div className="text-white">
                    <div className="text-xs font-semibold text-emerald-300">📊 PREDICTIONS</div>
                    <div className="text-sm font-bold">AI Match Predictions</div>
                    <div className="text-xs opacity-90">85% Accuracy Rate</div>
                  </div>
                  <div className="text-2xl">🤖</div>
                </div>
              </div>
            </div>

            {/* Slide 4 - Fantasy & Games */}
            <div className="min-w-full px-4">
              <div className="flex items-center gap-3 overflow-x-auto pb-2">
                <div className="flex items-center gap-2 bg-purple-500/30 rounded-lg px-4 py-2 backdrop-blur-sm flex-shrink-0 border border-purple-400/20">
                  <div className="text-white">
                    <div className="text-xs font-semibold text-purple-300">🏆 FANTASY</div>
                    <div className="text-sm font-bold">Fantasy League</div>
                    <div className="text-xs opacity-90">Win ₦1M Weekly</div>
                  </div>
                  <div className="text-2xl">👑</div>
                </div>

                <div className="flex items-center gap-2 bg-amber-500/30 rounded-lg px-4 py-2 backdrop-blur-sm flex-shrink-0 border border-amber-400/20">
                  <div className="text-white">
                    <div className="text-xs font-semibold text-amber-300">🎮 MINI GAMES</div>
                    <div className="text-sm font-bold">Play & Win</div>
                    <div className="text-xs opacity-90">Instant Prizes</div>
                  </div>
                  <div className="text-2xl">🎯</div>
                </div>

                <div className="flex items-center gap-2 bg-rose-500/30 rounded-lg px-4 py-2 backdrop-blur-sm flex-shrink-0 border border-rose-400/20">
                  <div className="text-white">
                    <div className="text-xs font-semibold text-rose-300">🎪 TOURNAMENTS</div>
                    <div className="text-sm font-bold">Weekly Contests</div>
                    <div className="text-xs opacity-90">Big Prizes</div>
                  </div>
                  <div className="text-2xl">🏆</div>
                </div>

                <div className="flex items-center gap-2 bg-violet-500/30 rounded-lg px-4 py-2 backdrop-blur-sm flex-shrink-0 border border-violet-400/20">
                  <div className="text-white">
                    <div className="text-xs font-semibold text-violet-300">🎊 JACKPOT</div>
                    <div className="text-sm font-bold">Progressive Jackpot</div>
                    <div className="text-xs opacity-90">₦50M+ Prize Pool</div>
                  </div>
                  <div className="text-2xl">💎</div>
                </div>

                <div className="flex items-center gap-2 bg-slate-500/30 rounded-lg px-4 py-2 backdrop-blur-sm flex-shrink-0 border border-slate-400/20">
                  <div className="text-white">
                    <div className="text-xs font-semibold text-slate-300">🎮 ESPORTS</div>
                    <div className="text-sm font-bold">Esports Betting</div>
                    <div className="text-xs opacity-90">FIFA, CS:GO & More</div>
                  </div>
                  <div className="text-2xl">🕹️</div>
                </div>
              </div>
            </div>

            {/* Slide 5 - Quick Betting & Features */}
            <div className="min-w-full px-4">
              <div className="flex items-center gap-3 overflow-x-auto pb-2">
                <div className="flex items-center gap-2 bg-cyan-500/30 rounded-lg px-4 py-2 backdrop-blur-sm flex-shrink-0 border border-cyan-400/20">
                  <div className="text-white">
                    <div className="text-xs font-semibold text-cyan-300">⚡ QUICK BET</div>
                    <div className="text-sm font-bold">One-Click Betting</div>
                    <div className="text-xs opacity-90">Bet in Seconds</div>
                  </div>
                  <div className="text-2xl">⚡</div>
                </div>

                <div className="flex items-center gap-2 bg-emerald-500/30 rounded-lg px-4 py-2 backdrop-blur-sm flex-shrink-0 border border-emerald-400/20">
                  <div className="text-white">
                    <div className="text-xs font-semibold text-emerald-300">💰 CASH OUT</div>
                    <div className="text-sm font-bold">Early Cash Out</div>
                    <div className="text-xs opacity-90">Secure Your Wins</div>
                  </div>
                  <div className="text-2xl">💸</div>
                </div>

                <div className="flex items-center gap-2 bg-sky-500/30 rounded-lg px-4 py-2 backdrop-blur-sm flex-shrink-0 border border-sky-400/20">
                  <div className="text-white">
                    <div className="text-xs font-semibold text-sky-300">📱 MOBILE APP</div>
                    <div className="text-sm font-bold">Download App</div>
                    <div className="text-xs opacity-90">Bet Anywhere</div>
                  </div>
                  <div className="text-2xl">📲</div>
                </div>

                <div className="flex items-center gap-2 bg-fuchsia-500/30 rounded-lg px-4 py-2 backdrop-blur-sm flex-shrink-0 border border-fuchsia-400/20">
                  <div className="text-white">
                    <div className="text-xs font-semibold text-fuchsia-300">🔒 SECURE</div>
                    <div className="text-sm font-bold">Safe & Secure</div>
                    <div className="text-xs opacity-90">SSL Protected</div>
                  </div>
                  <div className="text-2xl">🛡️</div>
                </div>

                <div className="flex items-center gap-2 bg-zinc-500/30 rounded-lg px-4 py-2 backdrop-blur-sm flex-shrink-0 border border-zinc-400/20">
                  <div className="text-white">
                    <div className="text-xs font-semibold text-zinc-300">💳 PAYMENT</div>
                    <div className="text-sm font-bold">Instant Deposits</div>
                    <div className="text-xs opacity-90">Bank Transfer & Cards</div>
                  </div>
                  <div className="text-2xl">💰</div>
                </div>
              </div>
            </div>

            {/* Slide 6 - Hot Matches & Promotions */}
            <div className="min-w-full px-4">
              <div className="flex items-center gap-3 overflow-x-auto pb-2">
                <div className="flex items-center gap-2 bg-orange-500/30 rounded-lg px-4 py-2 backdrop-blur-sm flex-shrink-0 border border-orange-400/20">
                  <div className="text-white">
                    <div className="text-xs font-semibold text-orange-300">🔥 HOT MATCH</div>
                    <div className="text-sm font-bold">
                      {matches.length > 0 ? `${matches[0].home_team} vs ${matches[0].away_team}` : 'Big Match Today'}
                    </div>
                    <div className="text-xs opacity-90">
                      {matches.length > 0 ? `Best Odds: ${matches[0].home_odds.toFixed(2)}` : "Don't Miss Out!"}
                    </div>
                  </div>
                  <div className="text-2xl">⚽</div>
                </div>

                <div className="flex items-center gap-2 bg-red-500/30 rounded-lg px-4 py-2 backdrop-blur-sm flex-shrink-0 border border-red-400/20">
                  <div className="text-white">
                    <div className="text-xs font-semibold text-red-300">🚀 BOOST</div>
                    <div className="text-sm font-bold">Odds Boost</div>
                    <div className="text-xs opacity-90">Enhanced Odds</div>
                  </div>
                  <div className="text-2xl">📈</div>
                </div>

                <div className="flex items-center gap-2 bg-yellow-500/30 rounded-lg px-4 py-2 backdrop-blur-sm flex-shrink-0 border border-yellow-400/20">
                  <div className="text-white">
                    <div className="text-xs font-semibold text-yellow-300">⏰ LIMITED</div>
                    <div className="text-sm font-bold">Flash Promo</div>
                    <div className="text-xs opacity-90">24 Hours Only</div>
                  </div>
                  <div className="text-2xl">⚡</div>
                </div>

                <div className="flex items-center gap-2 bg-green-500/30 rounded-lg px-4 py-2 backdrop-blur-sm flex-shrink-0 border border-green-400/20">
                  <div className="text-white">
                    <div className="text-xs font-semibold text-green-300">🎉 WEEKEND</div>
                    <div className="text-sm font-bold">Weekend Special</div>
                    <div className="text-xs opacity-90">Double Rewards</div>
                  </div>
                  <div className="text-2xl">🎊</div>
                </div>

                <div className="flex items-center gap-2 bg-stone-500/30 rounded-lg px-4 py-2 backdrop-blur-sm flex-shrink-0 border border-stone-400/20">
                  <div className="text-white">
                    <div className="text-xs font-semibold text-stone-300">🏆 LEAGUES</div>
                    <div className="text-sm font-bold">All Major Leagues</div>
                    <div className="text-xs opacity-90">EPL, La Liga, Serie A</div>
                  </div>
                  <div className="text-2xl">⚽</div>
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
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 relative z-10">
        
        {/* Date Selector */}
        <div className="mb-6">
          <DateSelector 
            selectedDate={selectedDate}
            onDateChange={setSelectedDate}
            daysToShow={14}
          />
        </div>



        {/* Error Message */}
        {error && (
          <div className="mb-6 bg-danger/20 border border-danger rounded-card p-4">
            <div className="flex items-start gap-3">
              <div className="text-danger text-2xl">⚠️</div>
              <div className="flex-1">
                <h3 className="text-danger font-semibold mb-1">Error Loading Data</h3>
                <p className="text-danger/90 text-sm mb-3">{error}</p>
                <button
                  onClick={() => loadData()}
                  className="px-4 py-2 bg-danger hover:bg-danger/90 text-white rounded-lg font-semibold text-sm transition-all"
                >
                  Retry
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Matches - Responsive Layout */}
        {/* Desktop: Table View (hidden on mobile) */}
        <div className="hidden md:block">
          <MatchTable
            matches={matches}
            selectedDate={selectedDate}
            loading={loading}
            onBetClick={handleBetClick}
          />
        </div>

        {/* Mobile: Card View (hidden on desktop) */}
        <div className="block md:hidden">
          <MatchCardList
            matches={matches}
            selectedDate={selectedDate}
            loading={loading}
            onBetClick={handleBetClick}
          />
        </div>
        </main>

        {/* Betting Modal */}
        <BettingModal
          isOpen={bettingModalOpen}
          onClose={() => setBettingModalOpen(false)}
          match={selectedMatch}
          selectedBetType={selectedBetType}
          walletBalance={wallet?.balance || 0}
          onPlaceBet={handlePlaceBet}
          onTopUp={handleTopUp}
        />
      </div>

      {/* Quick Access Sidebar */}
        {bottomMenuOpen && activeBottomTab === 'quick-access' && (
          <div className="fixed inset-0 z-50 flex">
            {/* Sidebar */}
            <div className="w-80 bg-gradient-to-b from-gray-900 via-gray-800 to-gray-900 border-r border-gray-600 shadow-2xl overflow-y-auto transform transition-transform duration-300 ease-out">
              <div className="p-6">
                {/* Sidebar Header */}
                <div className="flex items-center justify-between mb-6">
                  <div>
                    <h2 className="text-lg font-bold text-white mb-1">Quick Access</h2>
                    <div className="w-12 h-1 bg-gradient-to-r from-cyan to-primary rounded-full"></div>
                  </div>
                  <button
                    onClick={() => setBottomMenuOpen(false)}
                    className="p-2 hover:bg-gray-700 rounded-lg transition-all"
                  >
                    <span className="text-gray-400 hover:text-white text-xl">✕</span>
                  </button>
                </div>

                {/* Main Navigation */}
                <div className="mb-6">
                  <div className="space-y-2">
                    <Link href="/dashboard" className="flex items-center gap-3 px-4 py-3 rounded-lg bg-primary/20 text-primary font-semibold transition-all hover:bg-primary/30">
                      <span className="text-xl">⚽</span>
                      <span>Live Matches</span>
                    </Link>
                    <Link href="/fantasy" className="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-gray-700 text-gray-300 hover:text-white transition-all">
                      <span className="text-xl">🏆</span>
                      <span>Fantasy League</span>
                    </Link>
                    <Link href="/bets" className="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-gray-700 text-gray-300 hover:text-white transition-all">
                      <span className="text-xl">🎯</span>
                      <span>My Bets</span>
                    </Link>
                    <Link href="/wallet" className="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-gray-700 text-gray-300 hover:text-white transition-all">
                      <span className="text-xl">💰</span>
                      <span>Wallet</span>
                    </Link>
                    <Link href="/profile" className="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-gray-700 text-gray-300 hover:text-white transition-all">
                      <span className="text-xl">👤</span>
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
                  <div className="grid grid-cols-2 gap-3">
                    <Link href="/live" className="bg-gradient-to-r from-red-600 to-red-700 hover:from-red-500 hover:to-red-600 p-3 rounded-lg text-center transition-all transform hover:scale-105">
                      <div className="text-xl mb-1">🔴</div>
                      <div className="text-white font-semibold text-xs">Live</div>
                    </Link>
                    <Link href="/popular" className="bg-gradient-to-r from-orange-600 to-orange-700 hover:from-orange-500 hover:to-orange-600 p-3 rounded-lg text-center transition-all transform hover:scale-105">
                      <div className="text-xl mb-1">🔥</div>
                      <div className="text-white font-semibold text-xs">Popular</div>
                    </Link>
                    <Link href="/casino" className="bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-500 hover:to-purple-600 p-3 rounded-lg text-center transition-all transform hover:scale-105">
                      <div className="text-xl mb-1">🎰</div>
                      <div className="text-white font-semibold text-xs">Casino</div>
                    </Link>
                    <Link href="/promotions" className="bg-gradient-to-r from-green-600 to-green-700 hover:from-green-500 hover:to-green-600 p-3 rounded-lg text-center transition-all transform hover:scale-105">
                      <div className="text-xl mb-1">🎁</div>
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
            <div className="bg-gradient-to-t from-gray-900 via-gray-800 to-gray-900 border-t border-gray-600 shadow-2xl">
              <div className="max-w-7xl mx-auto">
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
                    🎯 Betslip
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
                    📊 My Bets
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
                            <div className="text-4xl mb-3">🎲</div>
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
                          <div className="text-6xl mb-4">📊</div>
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
          <div className="bg-gradient-to-r from-gray-900 via-black to-gray-900 border-t border-gray-600 shadow-2xl">
            <div className="max-w-7xl mx-auto px-4 py-2">
              <div className="flex items-center justify-between">
                {/* A-Z Menu Button */}
                <button
                  onClick={() => {
                    setActiveBottomTab('quick-access');
                    setBottomMenuOpen(!bottomMenuOpen);
                  }}
                  className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-primary to-primary/80 hover:from-primary/90 hover:to-primary text-white rounded-lg font-bold transition-all transform hover:scale-105 shadow-lg"
                >
                  <span className="text-lg">📋</span>
                  <span>A-Z Menu</span>
                  <span className={`transform transition-transform ${bottomMenuOpen && activeBottomTab === 'quick-access' ? 'rotate-180' : ''}`}>
                    ▲
                  </span>
                </button>

                {/* Center Betslip Button */}
                <button
                  onClick={() => {
                    setActiveBottomTab('betslip');
                    setBottomMenuOpen(true);
                  }}
                  className="relative px-6 py-3 bg-gradient-to-r from-orange-600 to-orange-700 hover:from-orange-500 hover:to-orange-600 text-white rounded-lg font-bold transition-all transform hover:scale-105 shadow-lg"
                >
                  <span className="text-xl mr-2">🎯</span>
                  <span>Betslip</span>
                  {betslipItems.length > 0 && (
                    <span className="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full w-6 h-6 flex items-center justify-center font-bold">
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
                  className="relative flex items-center gap-2 px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg font-semibold transition-all transform hover:scale-105"
                >
                  <span className="text-lg">📊</span>
                  <span>My Bets</span>
                  {myBets.length > 0 && (
                    <span className="absolute -top-1 -right-1 bg-green-500 text-white text-xs rounded-full w-4 h-4 flex items-center justify-center">
                      {myBets.length}
                    </span>
                  )}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}