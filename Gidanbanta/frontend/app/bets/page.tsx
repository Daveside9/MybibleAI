'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuth } from '@/contexts/AuthContext';
import PageNavigation from '@/components/PageNavigation';

export default function BetsPage() {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !user) {
      router.push('/login');
    }
  }, [user, loading, router]);

  if (loading) {
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
    <div className="min-h-screen bg-navy">
      {/* Header */}
      <header className="bg-gradient-to-r from-primary to-primary-600 shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <h1 className="text-2xl font-bold text-white">My Bets</h1>
        </div>
      </header>

      {/* Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <PageNavigation />
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-navy-100 rounded-card p-6">
            <div className="flex items-center gap-3">
              <div className="text-3xl">🎯</div>
              <div>
                <div className="text-2xl font-bold text-text-primary">0</div>
                <div className="text-text-muted text-sm">Total Bets</div>
              </div>
            </div>
          </div>

          <div className="bg-navy-100 rounded-card p-6">
            <div className="flex items-center gap-3">
              <div className="text-3xl">💰</div>
              <div>
                <div className="text-2xl font-bold text-text-primary">₦0.00</div>
                <div className="text-text-muted text-sm">Total Wagered</div>
              </div>
            </div>
          </div>

          <div className="bg-navy-100 rounded-card p-6">
            <div className="flex items-center gap-3">
              <div className="text-3xl">🏆</div>
              <div>
                <div className="text-2xl font-bold text-success">₦0.00</div>
                <div className="text-text-muted text-sm">Total Won</div>
              </div>
            </div>
          </div>

          <div className="bg-navy-100 rounded-card p-6">
            <div className="flex items-center gap-3">
              <div className="text-3xl">📊</div>
              <div>
                <div className="text-2xl font-bold text-text-primary">0%</div>
                <div className="text-text-muted text-sm">Win Rate</div>
              </div>
            </div>
          </div>
        </div>

        {/* Filters */}
        <div className="bg-navy-100 rounded-card p-6 mb-6">
          <div className="flex flex-wrap gap-4 items-center">
            <div>
              <label className="block text-sm font-medium text-text-muted mb-1">Status</label>
              <select className="bg-navy-200 text-text-primary px-3 py-2 rounded-lg border border-navy-300 focus:border-primary focus:outline-none">
                <option value="">All Bets</option>
                <option value="pending">Pending</option>
                <option value="won">Won</option>
                <option value="lost">Lost</option>
                <option value="refunded">Refunded</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-text-muted mb-1">Date Range</label>
              <select className="bg-navy-200 text-text-primary px-3 py-2 rounded-lg border border-navy-300 focus:border-primary focus:outline-none">
                <option value="all">All Time</option>
                <option value="today">Today</option>
                <option value="week">This Week</option>
                <option value="month">This Month</option>
              </select>
            </div>

            <div className="flex-1"></div>

            <Link 
              href="/dashboard"
              className="px-4 py-2 bg-primary hover:bg-primary-600 text-white rounded-lg transition-colors"
            >
              Place New Bet
            </Link>
          </div>
        </div>

        {/* Bets Table */}
        <div className="bg-navy-100 rounded-card overflow-hidden">
          <div className="bg-primary px-6 py-3">
            <h2 className="text-white font-bold text-lg">Betting History</h2>
          </div>

          {/* Empty State */}
          <div className="p-12 text-center">
            <div className="text-6xl mb-4">🎯</div>
            <h3 className="text-xl font-semibold text-text-primary mb-2">No bets yet</h3>
            <p className="text-text-muted mb-6">
              You haven't placed any bets yet. Start by browsing matches and placing your first bet!
            </p>
            <Link 
              href="/dashboard"
              className="inline-flex items-center gap-2 px-6 py-3 bg-primary hover:bg-primary-600 text-white rounded-lg transition-colors"
            >
              <span>Browse Matches</span>
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </Link>
          </div>
        </div>

        {/* Responsible Gambling Notice */}
        <div className="mt-8 bg-warning/20 border border-warning/30 rounded-card p-4">
          <div className="flex items-start gap-3">
            <div className="text-warning text-xl">⚠️</div>
            <div>
              <h4 className="font-semibold text-warning mb-1">Responsible Gambling</h4>
              <p className="text-sm text-text-muted">
                Remember to gamble responsibly. Set limits on your betting and never bet more than you can afford to lose. 
                If you need help, visit our <Link href="/betting-limits" className="text-primary hover:underline">responsible gambling tools</Link>.
              </p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}