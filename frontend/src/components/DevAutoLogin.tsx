'use client';

// [SNIPPET]: surgicalfix + kenyafirst + refactorclean
// [CONTEXT]: Development auto-login helper for super admin supervision
// [GOAL]: Allow peter/normal and apollo/aluru742!! to auto-login for development supervision
// [TASK]: Create development helper component for quick login access

import React, { useState } from 'react';
import { useAuth } from '@/context/AuthContext';
import { useRouter } from 'next/navigation';

interface DevUser {
  username: string;
  password: string;
  role: string;
  description: string;
}

const DEV_USERS: DevUser[] = [
  {
    username: 'peter',
    password: 'normal',
    role: 'super_admin',
    description: 'Super Admin - Development Supervision'
  },
  {
    username: 'apollo',
    password: 'aluru742!!',
    role: 'user',
    description: 'User - Development Testing'
  }
];

export default function DevAutoLogin() {
  const [isLoading, setIsLoading] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const { login, isAuthenticated } = useAuth();
  const router = useRouter();

  // Only show in development mode and when not authenticated
  if (process.env.NODE_ENV !== 'development' || isAuthenticated) {
    return null;
  }

  const handleAutoLogin = async (user: DevUser) => {
    setIsLoading(user.username);
    setError(null);

    try {
      // Use the simple_api.py endpoints which are more likely to be running
      const loginEndpoint = user.role === 'super_admin'
        ? 'http://localhost:8000/superadmin/token'
        : 'http://localhost:8000/token';

      const response = await fetch(loginEndpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          username: user.username,
          password: user.password
        }) as unknown as BodyInit,
      });

      if (!response.ok) {
        let detail = 'Login failed';
        try {
          const errData = await response.json();
          detail = errData?.detail ?? detail;
        } catch {}
        throw new Error(`${detail} (${response.status})`);
      }

      const data = await response.json();
      const { access_token } = data;

      // For dev mode, create mock user data since backend might not have full user endpoint
      const userData = {
        id: user.username,
        username: user.username,
        email: `${user.username}@shujaa.studio`,
        role: user.role === 'super_admin' ? 'admin' : 'user',
        tenant_id: 'default'
      };

      // Use AuthContext login method
      login(access_token, userData);

      // Redirect based on role
      if (userData.role === 'admin') {
        router.push('/admin/dashboard');
      } else {
        router.push('/dashboard');
      }

    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Login failed');
      console.error('Auto-login error:', err);
    } finally {
      setIsLoading(null);
    }
  };

  return (
    <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3">
      <div className="text-xs font-bold text-yellow-800 mb-2">
        🔧 DEV MODE - Quick Login
      </div>
      
      {error && (
        <div className="text-xs text-red-600 mb-2 p-2 bg-red-50 rounded">
          {error}
        </div>
      )}

      <div className="space-y-2">
        {DEV_USERS.map((user) => (
          <button
            key={user.username}
            onClick={() => handleAutoLogin(user)}
            disabled={isLoading === user.username}
            className={`w-full text-left p-2 rounded text-xs transition-all duration-200 ${
              isLoading === user.username
                ? 'bg-gray-200 cursor-not-allowed'
                : 'bg-white hover:bg-gray-50 border border-gray-200 hover:border-gray-300'
            }`}
          >
            {isLoading === user.username ? (
              <div className="flex items-center space-x-2">
                <div className="w-3 h-3 border border-gray-400 border-t-transparent rounded-full animate-spin"></div>
                <span>Logging in...</span>
              </div>
            ) : (
              <div>
                <div className="font-semibold text-gray-800">
                  {user.username} ({user.role})
                </div>
                <div className="text-gray-600">
                  {user.description}
                </div>
              </div>
            )}
          </button>
        ))}
      </div>

      <div className="text-xs text-gray-500 mt-2 pt-2 border-t border-yellow-300">
        Development supervision access
      </div>
    </div>
  );
}
