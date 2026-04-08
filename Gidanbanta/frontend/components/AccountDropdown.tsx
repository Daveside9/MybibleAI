'use client';

import { useState, useRef, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

interface User {
  id: number;
  username: string;
  email: string;
  full_name?: string;
  role: string;
}

interface AccountDropdownProps {
  user: User;
  onLogout: () => void;
  onTopUp?: () => void;
}

export default function AccountDropdown({ user, onLogout, onTopUp }: AccountDropdownProps) {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const router = useRouter();

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const handleLogout = () => {
    setIsOpen(false);
    onLogout();
  };

  const menuItems = [
    {
      label: 'Deposit',
      action: () => {
        setIsOpen(false);
        onTopUp?.();
      },
      icon: '💳',
      description: 'Add funds to your account',
      isAction: true
    },
    {
      label: 'My Profile',
      href: '/profile',
      icon: '👤',
      description: 'View and edit your profile'
    },
    {
      label: 'My Bets',
      href: '/bets',
      icon: '🎯',
      description: 'View your betting history'
    },
    {
      label: 'Wallet',
      href: '/wallet',
      icon: '💰',
      description: 'Manage your funds'
    },
    {
      label: 'Account Settings',
      href: '/settings',
      icon: '⚙️',
      description: 'Manage your account preferences'
    },
    {
      label: 'Betting Limits',
      href: '/betting-limits',
      icon: '🛡️',
      description: 'Set responsible gambling limits'
    },
    {
      label: 'Transaction History',
      href: '/transactions',
      icon: '📊',
      description: 'View all your transactions'
    }
  ];

  // Add admin menu item if user is admin
  if (user.role === 'admin') {
    menuItems.push({
      label: 'Admin Panel',
      href: '/admin',
      icon: '🔧',
      description: 'System administration'
    });
  }

  return (
    <div className="relative z-[100]" ref={dropdownRef}>
      {/* Account Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 bg-white/10 hover:bg-white/20 backdrop-blur-sm px-4 py-2 rounded-lg border border-white/20 transition-all"
      >
        {/* User Info */}
        <div className="text-left">
          <div className="text-sm font-semibold text-white">
            My Account
          </div>
        </div>

        {/* Dropdown Arrow */}
        <div className={`text-white/70 transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`}>
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </div>
      </button>

      {/* Dropdown Menu */}
      {isOpen && (
        <div className="absolute right-0 mt-2 w-80 bg-white rounded-xl shadow-2xl border border-gray-200 py-2 z-50 animate-in slide-in-from-top-2 duration-200">
          {/* User Info Header */}
          <div className="px-4 py-3 border-b border-gray-100">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-gradient-to-br from-cyan to-primary rounded-full flex items-center justify-center text-white font-bold text-lg">
                {user.username.charAt(0).toUpperCase()}
              </div>
              <div>
                <div className="font-semibold text-gray-900">
                  {user.full_name || user.username}
                </div>
                <div className="text-sm text-gray-500">
                  {user.email}
                </div>
                <div className="text-xs text-primary font-medium capitalize">
                  {user.role === 'spectator' ? 'Spectator' : user.role}
                </div>
              </div>
            </div>
          </div>

          {/* Menu Items */}
          <div className="py-2">
            {menuItems.map((item, index) => {
              if (item.isAction) {
                return (
                  <button
                    key={index}
                    onClick={item.action}
                    className="flex items-center gap-3 px-4 py-3 hover:bg-gray-50 transition-colors group w-full text-left"
                  >
                    <div className="text-xl">{item.icon}</div>
                    <div className="flex-1">
                      <div className="font-medium text-gray-900 group-hover:text-primary">
                        {item.label}
                      </div>
                      <div className="text-xs text-gray-500">
                        {item.description}
                      </div>
                    </div>
                    <div className="text-gray-400 group-hover:text-primary">
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                      </svg>
                    </div>
                  </button>
                );
              }
              
              return (
                <Link
                  key={index}
                  href={item.href}
                  onClick={() => setIsOpen(false)}
                  className="flex items-center gap-3 px-4 py-3 hover:bg-gray-50 transition-colors group"
                >
                  <div className="text-xl">{item.icon}</div>
                  <div className="flex-1">
                    <div className="font-medium text-gray-900 group-hover:text-primary">
                      {item.label}
                    </div>
                    <div className="text-xs text-gray-500">
                      {item.description}
                    </div>
                  </div>
                  <div className="text-gray-400 group-hover:text-primary">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                  </div>
                </Link>
              );
            })}
          </div>

          {/* Logout Section */}
          <div className="border-t border-gray-100 pt-2">
            <button
              onClick={handleLogout}
              className="flex items-center gap-3 px-4 py-3 hover:bg-red-50 transition-colors group w-full text-left"
            >
              <div className="text-xl">🚪</div>
              <div className="flex-1">
                <div className="font-medium text-gray-900 group-hover:text-red-600">
                  Sign Out
                </div>
                <div className="text-xs text-gray-500">
                  Sign out of your account
                </div>
              </div>
              <div className="text-gray-400 group-hover:text-red-600">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
              </div>
            </button>
          </div>
        </div>
      )}
    </div>
  );
}