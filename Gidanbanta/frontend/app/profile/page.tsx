'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuth } from '@/contexts/AuthContext';
import PageNavigation from '@/components/PageNavigation';

export default function ProfilePage() {
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
          <h1 className="text-2xl font-bold text-white">My Profile</h1>
        </div>
      </header>

      {/* Content */}
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <PageNavigation />
        <div className="bg-navy-100 rounded-card p-6">
          <div className="flex items-center gap-6 mb-8">
            <div className="w-20 h-20 bg-gradient-to-br from-cyan to-primary rounded-full flex items-center justify-center text-white font-bold text-2xl">
              {user.username.charAt(0).toUpperCase()}
            </div>
            <div>
              <h2 className="text-2xl font-bold text-text-primary">{user.full_name || user.username}</h2>
              <p className="text-text-muted">{user.email}</p>
              <span className="inline-block px-3 py-1 bg-primary/20 text-primary rounded-full text-sm font-medium capitalize mt-2">
                {user.role === 'spectator' ? 'Spectator' : user.role}
              </span>
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-6">
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-text-primary">Account Information</h3>
              
              <div>
                <label className="block text-sm font-medium text-text-muted mb-1">Username</label>
                <div className="bg-navy-200 px-3 py-2 rounded-lg text-text-primary">
                  {user.username}
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-text-muted mb-1">Email</label>
                <div className="bg-navy-200 px-3 py-2 rounded-lg text-text-primary">
                  {user.email}
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-text-muted mb-1">Full Name</label>
                <div className="bg-navy-200 px-3 py-2 rounded-lg text-text-primary">
                  {user.full_name || 'Not set'}
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-text-muted mb-1">Account Type</label>
                <div className="bg-navy-200 px-3 py-2 rounded-lg text-text-primary capitalize">
                  {user.role === 'spectator' ? 'Spectator' : user.role}
                </div>
              </div>
            </div>

            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-text-primary">Quick Actions</h3>
              
              <Link 
                href="/wallet"
                className="block bg-primary hover:bg-primary-600 text-white px-4 py-3 rounded-lg transition-colors"
              >
                <div className="flex items-center gap-3">
                  <span className="text-xl">💰</span>
                  <div>
                    <div className="font-semibold">Manage Wallet</div>
                    <div className="text-sm opacity-90">View balance and transactions</div>
                  </div>
                </div>
              </Link>

              <Link 
                href="/bets"
                className="block bg-cyan hover:bg-cyan/90 text-navy px-4 py-3 rounded-lg transition-colors"
              >
                <div className="flex items-center gap-3">
                  <span className="text-xl">🎯</span>
                  <div>
                    <div className="font-semibold">My Bets</div>
                    <div className="text-sm opacity-90">View betting history</div>
                  </div>
                </div>
              </Link>

              <Link 
                href="/settings"
                className="block bg-navy-200 hover:bg-navy-300 text-text-primary px-4 py-3 rounded-lg transition-colors"
              >
                <div className="flex items-center gap-3">
                  <span className="text-xl">⚙️</span>
                  <div>
                    <div className="font-semibold">Account Settings</div>
                    <div className="text-sm text-text-muted">Manage preferences</div>
                  </div>
                </div>
              </Link>

              <Link 
                href="/betting-limits"
                className="block bg-warning/20 hover:bg-warning/30 text-warning px-4 py-3 rounded-lg transition-colors"
              >
                <div className="flex items-center gap-3">
                  <span className="text-xl">🛡️</span>
                  <div>
                    <div className="font-semibold">Betting Limits</div>
                    <div className="text-sm opacity-90">Responsible gambling</div>
                  </div>
                </div>
              </Link>
            </div>
          </div>

          <div className="mt-8 pt-6 border-t border-navy-200">
            <p className="text-text-muted text-sm">
              Need to update your profile information? Contact support or visit account settings.
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}