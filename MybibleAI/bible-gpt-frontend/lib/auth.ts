"use client";

import { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { fetchAuthenticated } from '@/lib/api';

interface User {
  name: string;
  email: string;
}

export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const router = useRouter();

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const res = await fetchAuthenticated('/api/users/me');
        if (!res.ok) {
          throw new Error('Failed to fetch user');
        }
        const userData = await res.json();
        setUser(userData);
      } catch (error) {
        console.error(error);
        // If fetching user fails, token is likely invalid, so logout.
        logout();
      }
    };

    // Ensure a token exists before fetching
    if (localStorage.getItem('access_token')) {
      fetchUser();
    } else {
      router.push('/login');
    }
  }, [router]);

  const logout = useCallback(() => {
    localStorage.removeItem('access_token');
    setUser(null);
    router.push('/login');
  }, [router]);

  return { user, logout };
}

import Cookies from 'js-cookie';

export const getToken = (): string | null => {
  if (typeof document === 'undefined') return null;
  const match = document.cookie.match(new RegExp('(^| )token=([^;]+)'));
  return match ? match[2] : null;
};

export const setToken = (token: string) => {
  if (typeof document === 'undefined') return;
  // Set cookie to expire in 7 days
  const d = new Date();
  d.setTime(d.getTime() + (7*24*60*60*1000));
  const expires = "expires="+ d.toUTCString();
  document.cookie = `token=${token};${expires};path=/`;
};

export const removeToken = () => {
  if (typeof document === 'undefined') return;
  document.cookie = 'token=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
};

export const isAuthenticated = (): boolean => {
  return getToken() !== null;
};
