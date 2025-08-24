"use client";

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useRouter } from 'next/navigation';

interface User {
  id: string;
  username: string;
  email: string;
  role: string;
  tenant_id: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (token: string, user: User) => void;
  logout: () => void;
  fetchUser: () => Promise<void>; // Function to re-fetch user data
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  // Users/roles that must be force-logged-out for security
  const FORCE_LOGOUT_USERNAMES = new Set(['peter', 'apollo']);
  const FORCE_LOGOUT_ROLES = new Set(['super_admin']);

  const shouldForceLogout = (u: User | null) => {
    if (!u) return false;
    const uname = (u.username || '').toLowerCase();
    const role = (u.role || '').toLowerCase();
    return FORCE_LOGOUT_USERNAMES.has(uname) || FORCE_LOGOUT_ROLES.has(role);
  };

  const fetchUser = async () => {
    setIsLoading(true);
    const storedToken = localStorage.getItem('jwt_token');
    if (storedToken) {
      try {
        const response = await fetch('http://localhost:8000/users/me', {
          headers: {
            'Authorization': `Bearer ${storedToken}`,
          },
        });

        if (response.ok) {
          const userData = await response.json();
          setUser(userData);
          setToken(storedToken);
          // Security guard: auto-logout restricted users/roles
          if (shouldForceLogout(userData)) {
            logout();
            return;
          }
        } else {
          localStorage.removeItem('jwt_token');
          setUser(null);
          setToken(null);
        }
      } catch (error) {
        console.error("Failed to fetch user data:", error);
        localStorage.removeItem('jwt_token');
        setUser(null);
        setToken(null);
      } finally {
        setIsLoading(false);
      }
    } else {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchUser();
  }, []);

  const login = (newToken: string, newUser: User) => {
    localStorage.setItem('jwt_token', newToken);
    setToken(newToken);
    setUser(newUser);
    // Security guard: auto-logout restricted users/roles
    if (shouldForceLogout(newUser)) {
      logout();
      return;
    }
  };

  const logout = () => {
    localStorage.removeItem('jwt_token');
    setToken(null);
    setUser(null);
    router.push('/login'); // Redirect to login page on logout
  };

  const isAuthenticated = !!user && !!token;

  return (
    <AuthContext.Provider value={{ user, token, isAuthenticated, isLoading, login, logout, fetchUser }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
