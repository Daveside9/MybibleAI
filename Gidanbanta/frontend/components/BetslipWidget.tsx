'use client';

import { useState } from 'react';

interface BetSelection {
  matchId: number;
  homeTeam: string;
  awayTeam: string;
  betType: 'home' | 'draw' | 'away';
  odds: number;
  league: string;
}

interface BetslipWidgetProps {
  selections: BetSelection[];
  onRemove: (matchId: number) => void;
  onClear: () => void;
  onPlaceBet: (stake: number) => void;
  walletBalance: number;
}

export default function BetslipWidget({
  selections,
  onRemove,
  onClear,
  onPlaceBet,
  walletBalance
}: BetslipWidgetProps) {
  const [stake, setStake] = useState<string>('');
  const [isExpanded, setIsExpanded] = useState(true);

  // Calculate total odds (multiply all odds together for accumulator)
  const totalOdds = selections.reduce((acc, sel) => acc * sel.odds, 1);
  
  // Calculate potential winnings
  const potentialWin = stake ? (parseFloat(stake) * totalOdds).toFixed(2) : '0.00';

  const getBetTypeLabel = (betType: 'home' | 'draw' | 'away', homeTeam: string, awayTeam: string) => {
    if (betType === 'home') return homeTeam;
    if (betType === 'away') return awayTeam;
    return 'Draw';
  };

  const handlePlaceBet = () => {
    const stakeAmount = parseFloat(stake);
    if (isNaN(stakeAmount) || stakeAmount <= 0) {
      alert('Please enter a valid stake amount');
      return;
    }
    if (stakeAmount > walletBalance) {
      alert('Insufficient balance');
      return;
    }
    onPlaceBet(stakeAmount);
    setStake('');
  };

  if (selections.length === 0) {
    return null;
  }

  return (
    <div className="fixed bottom-20 right-4 z-50 w-96 max-h-[600px] bg-gradient-to-b from-gray-900 via-gray-800 to-gray-900 rounded-lg shadow-2xl border border-white/20 overflow-hidden">
      {/* Header */}
      <div className="bg-black/40 backdrop-blur-md px-4 py-3 border-b border-white/10 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="text-2xl">🎫</span>
          <div>
            <h3 className="text-white font-bold text-sm" style={{ textShadow: '0 4px 6px rgba(0, 0, 139, 0.8), 0 2px 4px rgba(0, 0, 139, 0.6)' }}>
              Betslip
            </h3>
            <p className="text-gray-400 text-xs">{selections.length} {selections.length === 1 ? 'selection' : 'selections'}</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="p-1 hover:bg-white/10 rounded transition-all"
          >
            <span className="text-white text-lg">{isExpanded ? '▼' : '▲'}</span>
          </button>
          <button
            onClick={onClear}
            className="p-1 hover:bg-red-600/20 rounded transition-all"
          >
            <span className="text-red-400 text-lg">✕</span>
          </button>
        </div>
      </div>

      {isExpanded && (
        <>
          {/* Selections List */}
          <div className="max-h-64 overflow-y-auto p-3 space-y-2">
            {selections.map((selection) => (
              <div
                key={selection.matchId}
                className="bg-black/30 backdrop-blur-sm rounded-lg p-3 border border-white/10 hover:border-white/20 transition-all"
              >
                <div className="flex items-start justify-between mb-2">
                  <div className="flex-1">
                    <div className="text-white text-xs font-semibold mb-1">
                      {selection.homeTeam} vs {selection.awayTeam}
                    </div>
                    <div className="text-gray-400 text-xs">{selection.league}</div>
                  </div>
                  <button
                    onClick={() => onRemove(selection.matchId)}
                    className="text-red-400 hover:text-red-300 text-sm ml-2"
                  >
                    ✕
                  </button>
                </div>
                <div className="flex items-center justify-between">
                  <div className="bg-blue-600/20 px-2 py-1 rounded">
                    <span className="text-blue-300 text-xs font-bold">
                      {getBetTypeLabel(selection.betType, selection.homeTeam, selection.awayTeam)}
                    </span>
                  </div>
                  <div className="text-green-400 font-bold text-sm">
                    {selection.odds.toFixed(2)}
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Bet Summary */}
          <div className="bg-black/40 backdrop-blur-md p-4 border-t border-white/10">
            {/* Total Odds */}
            <div className="flex items-center justify-between mb-3">
              <span className="text-gray-300 text-sm font-semibold">Total Odds:</span>
              <span className="text-green-400 font-bold text-lg">{totalOdds.toFixed(2)}</span>
            </div>

            {/* Stake Input */}
            <div className="mb-3">
              <label className="text-gray-300 text-xs font-semibold mb-1 block">Stake Amount (₦)</label>
              <input
                type="number"
                value={stake}
                onChange={(e) => setStake(e.target.value)}
                placeholder="Enter stake..."
                className="w-full px-3 py-2 bg-black/30 border border-white/20 rounded-lg text-white text-sm focus:border-blue-500 focus:outline-none"
                min="0"
                step="100"
              />
              <div className="flex items-center justify-between mt-1">
                <span className="text-gray-400 text-xs">Balance: ₦{walletBalance.toFixed(2)}</span>
                <div className="flex gap-1">
                  <button
                    onClick={() => setStake('100')}
                    className="px-2 py-0.5 bg-gray-700 hover:bg-gray-600 text-white text-xs rounded transition-all"
                  >
                    ₦100
                  </button>
                  <button
                    onClick={() => setStake('500')}
                    className="px-2 py-0.5 bg-gray-700 hover:bg-gray-600 text-white text-xs rounded transition-all"
                  >
                    ₦500
                  </button>
                  <button
                    onClick={() => setStake('1000')}
                    className="px-2 py-0.5 bg-gray-700 hover:bg-gray-600 text-white text-xs rounded transition-all"
                  >
                    ₦1K
                  </button>
                </div>
              </div>
            </div>

            {/* Potential Win */}
            <div className="bg-gradient-to-r from-green-600/20 to-emerald-600/20 rounded-lg p-3 mb-3 border border-green-500/30">
              <div className="flex items-center justify-between">
                <span className="text-green-300 text-sm font-semibold">Potential Win:</span>
                <span className="text-green-400 font-bold text-xl">₦{potentialWin}</span>
              </div>
            </div>

            {/* Place Bet Button */}
            <button
              onClick={handlePlaceBet}
              disabled={!stake || parseFloat(stake) <= 0}
              className="w-full py-3 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-500 hover:to-blue-600 disabled:from-gray-600 disabled:to-gray-700 disabled:cursor-not-allowed text-white font-bold rounded-lg transition-all transform hover:scale-105 disabled:hover:scale-100 shadow-lg"
              style={{ textShadow: '0 2px 4px rgba(0, 0, 0, 0.5)' }}
            >
              Place Bet
            </button>
          </div>
        </>
      )}
    </div>
  );
}
