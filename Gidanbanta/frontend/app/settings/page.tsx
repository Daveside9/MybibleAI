'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuth } from '@/contexts/AuthContext';
import PageNavigation from '@/components/PageNavigation';

export default function SettingsPage() {
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
          <h1 className="text-2xl font-bold text-white">Account Settings</h1>
        </div>
      </header>

      {/* Content */}
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <PageNavigation />
        <div className="space-y-6">
          
          {/* Profile Settings */}
          <div className="bg-navy-100 rounded-card p-6">
            <h2 className="text-xl font-semibold text-text-primary mb-4">Profile Settings</h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-text-muted mb-1">Full Name</label>
                <input 
                  type="text" 
                  defaultValue={user.full_name || ''}
                  className="w-full bg-navy-200 text-text-primary px-3 py-2 rounded-lg border border-navy-300 focus:border-primary focus:outline-none"
                  placeholder="Enter your full name"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-text-muted mb-1">Email</label>
                <input 
                  type="email" 
                  defaultValue={user.email}
                  className="w-full bg-navy-200 text-text-primary px-3 py-2 rounded-lg border border-navy-300 focus:border-primary focus:outline-none"
                />
              </div>

              <button className="px-4 py-2 bg-primary hover:bg-primary-600 text-white rounded-lg transition-colors">
                Update Profile
              </button>
            </div>
          </div>

          {/* Security Settings */}
          <div className="bg-navy-100 rounded-card p-6">
            <h2 className="text-xl font-semibold text-text-primary mb-4">Security</h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-text-muted mb-1">Current Password</label>
                <input 
                  type="password" 
                  className="w-full bg-navy-200 text-text-primary px-3 py-2 rounded-lg border border-navy-300 focus:border-primary focus:outline-none"
                  placeholder="Enter current password"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-text-muted mb-1">New Password</label>
                <input 
                  type="password" 
                  className="w-full bg-navy-200 text-text-primary px-3 py-2 rounded-lg border border-navy-300 focus:border-primary focus:outline-none"
                  placeholder="Enter new password"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-text-muted mb-1">Confirm New Password</label>
                <input 
                  type="password" 
                  className="w-full bg-navy-200 text-text-primary px-3 py-2 rounded-lg border border-navy-300 focus:border-primary focus:outline-none"
                  placeholder="Confirm new password"
                />
              </div>

              <button className="px-4 py-2 bg-primary hover:bg-primary-600 text-white rounded-lg transition-colors">
                Change Password
              </button>
            </div>
          </div>

          {/* Notification Settings */}
          <div className="bg-navy-100 rounded-card p-6">
            <h2 className="text-xl font-semibold text-text-primary mb-4">Notifications</h2>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <div className="font-medium text-text-primary">Bet Results</div>
                  <div className="text-sm text-text-muted">Get notified when your bets are settled</div>
                </div>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input type="checkbox" className="sr-only peer" defaultChecked />
                  <div className="w-11 h-6 bg-navy-300 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
                </label>
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <div className="font-medium text-text-primary">Match Updates</div>
                  <div className="text-sm text-text-muted">Live score updates for matches you bet on</div>
                </div>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input type="checkbox" className="sr-only peer" defaultChecked />
                  <div className="w-11 h-6 bg-navy-300 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
                </label>
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <div className="font-medium text-text-primary">Promotions</div>
                  <div className="text-sm text-text-muted">Special offers and bonus notifications</div>
                </div>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input type="checkbox" className="sr-only peer" />
                  <div className="w-11 h-6 bg-navy-300 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
                </label>
              </div>
            </div>
          </div>

          {/* Privacy Settings */}
          <div className="bg-navy-100 rounded-card p-6">
            <h2 className="text-xl font-semibold text-text-primary mb-4">Privacy</h2>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <div className="font-medium text-text-primary">Profile Visibility</div>
                  <div className="text-sm text-text-muted">Allow other users to see your profile</div>
                </div>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input type="checkbox" className="sr-only peer" />
                  <div className="w-11 h-6 bg-navy-300 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
                </label>
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <div className="font-medium text-text-primary">Analytics</div>
                  <div className="text-sm text-text-muted">Help improve our service with usage data</div>
                </div>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input type="checkbox" className="sr-only peer" defaultChecked />
                  <div className="w-11 h-6 bg-navy-300 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
                </label>
              </div>
            </div>
          </div>

          {/* Danger Zone */}
          <div className="bg-danger/10 border border-danger/30 rounded-card p-6">
            <h2 className="text-xl font-semibold text-danger mb-4">Danger Zone</h2>
            <div className="space-y-4">
              <div>
                <h3 className="font-medium text-text-primary mb-2">Delete Account</h3>
                <p className="text-sm text-text-muted mb-4">
                  Once you delete your account, there is no going back. Please be certain.
                </p>
                <button className="px-4 py-2 bg-danger hover:bg-danger/90 text-white rounded-lg transition-colors">
                  Delete Account
                </button>
              </div>
            </div>
          </div>

        </div>
      </main>
    </div>
  );
}