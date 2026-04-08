'use client';

import { useState, useEffect } from 'react';
import { formatMatchTime } from '@/lib/timeUtils';

interface Match {
  id: number;
  home_team: string;
  away_team: string;
  home_odds: number;
  away_odds: number;
  draw_odds: number;
  scheduled_time: string;
  league?: {
    name: string;
  } | null;
}

interface BettingModalProps {
  isOpen: boolean;
  onClose: () => void;
  match: Match | null;
  selectedBetType?: 'home' | 'draw' | 'away';
  walletBalance: number;
  onPlaceBet: (matchId: number, betType: 'home' | 'draw' | 'away', stake: number) => Promise<void>;
  onTopUp: () => void;
}

export default function BettingModal({
  isOpen,
  onClose,
  match,
  selectedBetType = 'home',
  walletBalance,
  onPlaceBet,
  onTopUp
}: BettingModalProps) {
  const [betType, setBetType] = useState<'home' | 'draw' | 'away'>(selectedBetType);
  const [stake, setStake] = useState<string>('');
  const [isPlacing, setIsPlacing] = useState(false);
  const [error, setError] = useState<string>('');

  // Update bet type when prop changes
  useEffect(() => {
    setBetType(selectedBetType);
  }, [selectedBetType]);

  // Reset state when modal opens/closes
  useEffect(() => {
    if (isOpen) {
      setStake('');
      setError('');
      setIsPlacing(false);
    }
  }, [isOpen]);

  if (!isOpen || !match) return null;

  const getOdds = () => {
    switch (betType) {
      case 'home':
        return match.home_odds;
      case 'draw':
        return match.draw_odds;
      case 'away':
        return match.away_odds;
    }
  };

  const getBetLabel = () => {
    switch (betType) {
      case 'home':
        return match.home_team;
      case 'draw':
        return 'Draw';
      case 'away':
        return match.away_team;
    }
  };

  const calculatePotentialWinnings = () => {
    const stakeAmount = parseFloat(stake) || 0;
    const odds = getOdds();
    return (stakeAmount * odds).toFixed(2);
  };

  const handleStakeChange = (value: string) => {
    // Only allow numbers and decimal point
    if (value === '' || /^\d*\.?\d*$/.test(value)) {
      setStake(value);
      setError('');
    }
  };

  const handleQuickStake = (amount: number) => {
    setStake(amount.toString());
    setError('');
  };

  const handlePlaceBet = async () => {
    const stakeAmount = parseFloat(stake);

    // Validation
    if (!stake || stakeAmount <= 0) {
      setError('Please enter a valid stake amount');
      return;
    }

    if (stakeAmount > walletBalance) {
      setError('Insufficient balance');
      return;
    }

    if (stakeAmount < 10) {
      setError('Minimum stake is ₦10');
      return;
    }

    setIsPlacing(true);
    setError('');

    try {
      await onPlaceBet(match.id, betType, stakeAmount);
      onClose();
    } catch (err: any) {
      setError(err.message || 'Failed to place bet');
    } finally {
      setIsPlacing(false);
    }
  };

  const insufficientBalance = parseFloat(stake) > walletBalance;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm">
      <div className="bg-navy-100 rounded-card max-w-md w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="bg-primary px-6 py-4 flex items-center justify-between sticky top-0">
          <h2 className="text-white font-bold text-lg">Place Bet</h2>
          <button
            onClick={onClose}
            className="text-white/80 hover:text-white text-2xl leading-none"
            aria-label="Close modal"
          >
            ×
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Match Info */}
          <div className="bg-navy-200 rounded-lg p-4">
            <div className="text-text-muted text-sm mb-2">
              {match.league?.name} • {formatMatchTime(match.scheduled_time)}
            </div>
            <div className="text-text-primary font-semibold text-lg">
              {match.home_team} vs {match.away_team}
            </div>
          </div>

          {/* Bet Type Selection */}
          <div>
            <label className="text-text-primary font-semibold mb-3 block">
              Select Outcome
            </label>
            <div className="grid grid-cols-3 gap-2">
              <button
                onClick={() => setBetType('home')}
                className={`py-3 rounded-lg transition-all ${
                  betType === 'home'
                    ? 'bg-primary text-white'
                    : 'bg-navy-200 text-text-muted hover:bg-navy-300'
                }`}
              >
                <div className="text-xs mb-1">Home</div>
                <div className="font-bold">{match.home_odds.toFixed(2)}</div>
              </button>
              <button
                onClick={() => setBetType('draw')}
                className={`py-3 rounded-lg transition-all ${
                  betType === 'draw'
                    ? 'bg-primary text-white'
                    : 'bg-navy-200 text-text-muted hover:bg-navy-300'
                }`}
              >
                <div className="text-xs mb-1">Draw</div>
                <div className="font-bold">{match.draw_odds.toFixed(2)}</div>
              </button>
              <button
                onClick={() => setBetType('away')}
                className={`py-3 rounded-lg transition-all ${
                  betType === 'away'
                    ? 'bg-primary text-white'
                    : 'bg-navy-200 text-text-muted hover:bg-navy-300'
                }`}
              >
                <div className="text-xs mb-1">Away</div>
                <div className="font-bold">{match.away_odds.toFixed(2)}</div>
              </button>
            </div>
          </div>

          {/* Stake Input */}
          <div>
            <label className="text-text-primary font-semibold mb-2 block">
              Stake Amount
            </label>
            <div className="relative">
              <span className="absolute left-4 top-1/2 -translate-y-1/2 text-text-muted">
                ₦
              </span>
              <input
                type="text"
                value={stake}
                onChange={(e) => handleStakeChange(e.target.value)}
                placeholder="0.00"
                className="w-full bg-navy-200 text-text-primary pl-10 pr-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
              />
            </div>
            <div className="mt-2 text-sm text-text-muted">
              Available: ₦{walletBalance.toFixed(2)}
            </div>
          </div>

          {/* Quick Stake Buttons */}
          <div className="grid grid-cols-4 gap-2">
            {[100, 500, 1000, 5000].map((amount) => (
              <button
                key={amount}
                onClick={() => handleQuickStake(amount)}
                className="py-2 bg-navy-200 hover:bg-navy-300 text-text-primary rounded-lg text-sm transition-all"
              >
                ₦{amount}
              </button>
            ))}
          </div>

          {/* Bet Summary */}
          <div className="bg-navy-200 rounded-lg p-4 space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-text-muted">Betting on:</span>
              <span className="text-text-primary font-semibold">{getBetLabel()}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-text-muted">Odds:</span>
              <span className="text-text-primary font-semibold">{getOdds().toFixed(2)}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-text-muted">Stake:</span>
              <span className="text-text-primary font-semibold">₦{stake || '0.00'}</span>
            </div>
            <div className="border-t border-navy-300 pt-2 mt-2">
              <div className="flex justify-between">
                <span className="text-text-primary font-semibold">Potential Winnings:</span>
                <span className="text-success font-bold text-lg">
                  ₦{calculatePotentialWinnings()}
                </span>
              </div>
            </div>
          </div>

          {/* Error Message */}
          {error && (
            <div className="bg-danger/20 border border-danger text-danger px-4 py-3 rounded-lg text-sm">
              {error}
            </div>
          )}

          {/* Insufficient Balance Warning */}
          {insufficientBalance && !error && (
            <div className="bg-warning/20 border border-warning text-warning px-4 py-3 rounded-lg text-sm">
              Insufficient balance. Please top up your wallet.
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex gap-3">
            {insufficientBalance ? (
              <button
                onClick={onTopUp}
                className="flex-1 py-3 bg-cyan hover:bg-cyan/90 text-navy rounded-lg font-bold transition-all"
              >
                Top Up Wallet
              </button>
            ) : (
              <>
                <button
                  onClick={onClose}
                  className="flex-1 py-3 bg-navy-300 hover:bg-navy-400 text-text-muted rounded-lg font-semibold transition-all"
                  disabled={isPlacing}
                >
                  Cancel
                </button>
                <button
                  onClick={handlePlaceBet}
                  disabled={isPlacing || !stake || parseFloat(stake) <= 0}
                  className="flex-1 py-3 bg-primary hover:bg-primary-600 text-white rounded-lg font-bold transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isPlacing ? 'Placing...' : 'Place Bet'}
                </button>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
