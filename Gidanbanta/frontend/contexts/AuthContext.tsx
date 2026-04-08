'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '@/lib/api';

interface User {
  id: number;
  email: string;
  username: string;
  full_name?: string;
  role: string;
  kyc_status: string;
  is_adult: boolean;
  can_purchase: boolean;
  created_at: string;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<{ success: boolean; error?: string }>;
  signup: (data: SignupData) => Promise<{ success: boolean; error?: string }>;
  logout: () => void;
}

interface SignupData {
  email: string;
  username: string;
  password: string;
  full_name?: string;
  date_of_birth: string;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      setLoading(false);
      return;
    }

    try {
      const response = await api.getCurrentUser();
      if (response.data) {
        setUser(response.data as User);
      } else if (response.error) {
        // Only clear tokens if we get a 401 auth error
        if (response.error.includes('401') || response.error.includes('Unauthorized') || response.error.includes('Could not validate credentials')) {
          console.log('Auth token invalid, clearing tokens');
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          setUser(null);
        } else {
          // For network errors or other issues, keep the user logged in
          console.log('Network error during auth check:', response.error);
        }
      }
    } catch (error) {
      console.error('Auth check error:', error);
      // Don't logout on network errors
    } finally {
      setLoading(false);
    }
  };

  const login = async (email: string, password: string) => {
    const response = await api.login({ email, password });
    
    if (response.error) {
      return { success: false, error: response.error };
    }

    const data = response.data as any;
    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('refresh_token', data.refresh_token);
    setUser(data.user);
    router.push('/dashboard');
    
    return { success: true };
  };

  const signup = async (signupData: SignupData) => {
    const response = await api.signup(signupData);
    
    if (response.error) {
      return { success: false, error: response.error };
    }

    const data = response.data as any;
    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('refresh_token', data.refresh_token);
    setUser(data.user);
    router.push('/dashboard');
    
    return { success: true };
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setUser(null);
    router.push('/login');
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, signup, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
