"use client";
import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import LoadingStates from '@/components/ui/LoadingStates';
import ErrorStates from '@/components/ui/ErrorStates';
import Card from '@/components/Card';

interface LoginPageProps {
  params?: Promise<{lang: string}>;
}

const LoginPage: React.FC<LoginPageProps> = ({ params }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);

    try {
      // Determine login endpoint based on username for superadmin
      const loginEndpoint = 'http://localhost:8000/token';

      const response = await fetch(loginEndpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({ username, password }) as unknown as BodyInit,
      });

      if (!response.ok) {
        // Try to parse error payload similar to FastAPI { detail: ... }
        let detail = 'Login failed';
        try { const errData = await response.json(); detail = errData?.detail ?? detail; } catch {}
        throw new Error(detail);
      }

      const data = await response.json();
      const { access_token } = data;
      localStorage.setItem('jwt_token', access_token); // Store token securely

      // Fetch user details to get the role
      const userResponse = await fetch('http://localhost:8000/users/me', {
        headers: {
          'Authorization': `Bearer ${access_token}`,
        },
      });

      if (!userResponse.ok) {
        throw new Error('Failed to fetch user details after login.');
      }

      const userData = await userResponse.json();
      const userRole = userData.role; // Assuming the /users/me endpoint returns a 'role' field

      if (userRole === 'admin') { // Assuming 'admin' is the role for super admins
        router.push('/admin/dashboard'); // Redirect to Super Admin Dashboard
      } else {
        router.push('/dashboard'); // Redirect to regular dashboard
      }

    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'An unexpected error occurred. Please try again.';
      setError(message);
      console.error('Login error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-50 to-yellow-50 px-4 py-8">
      <Card className="w-full max-w-md">
        <div className="p-8">
          {/* Kenya-first header */}
          <div className="text-center mb-8">
            <div className="flex justify-center items-center space-x-2 mb-4">
              <span className="text-3xl">🇰🇪</span>
              <h1 className="text-2xl font-bold text-gray-800">Shujaa Studio</h1>
            </div>
            <p className="text-gray-600">Welcome back to Kenya&apos;s AI Video Platform</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            {error && (
              <ErrorStates.Alert
                type="error"
                title="Login Failed"
                message={error}
                className="mb-4"
              />
            )}
            
            <div>
              <label htmlFor="username" className="block text-sm font-medium text-gray-700 mb-2">
                Username
              </label>
              <input
                type="text"
                id="username"
                className="form-input w-full p-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-green-500 focus:border-transparent"
                placeholder="Enter your username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                disabled={isLoading}
              />
            </div>
            
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
                Password
              </label>
              <input
                type="password"
                id="password"
                className="form-input w-full p-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-green-500 focus:border-transparent"
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                disabled={isLoading}
              />
            </div>
            
            <button
              type="submit"
              className="w-full bg-green-600 hover:bg-green-700 text-white font-semibold py-3 px-4 rounded-lg transition-colors duration-200 flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed"
              disabled={isLoading}
            >
              {isLoading ? (
                <>
                  <LoadingStates.LoadingSpinner size="sm" className="mr-2" />
                  Signing in...
                </>
              ) : (
                'Sign In 🇰🇪'
              )}
            </button>
          </form>
          
          <div className="mt-6 text-center">
            <p className="text-sm text-gray-600">
              Don&apos;t have an account?{' '}
              <Link href="/register" className="text-green-600 hover:text-green-800 font-medium transition-colors duration-200">
                Register here
              </Link>
            </p>
          </div>
        </div>
      </Card>
    </div>
  );
};

export default LoginPage; // Export as default for page component