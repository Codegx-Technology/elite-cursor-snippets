"use client";
import React, { useState } from 'react';
import { useRouter } from 'next/navigation'; // Use next/navigation for App Router

const LoginPage: React.FC = () => {
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
      const loginEndpoint = (username === 'peter' || username === 'apollo') 
        ? 'http://localhost:8000/superadmin/token' 
        : 'http://localhost:8000/token';

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

    } catch (err: any) {
      const message = err?.message || 'An unexpected error occurred. Please try again.';
      setError(message);
      console.error('Login error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="elite-card p-8 max-w-md mx-auto my-10 rounded-xl shadow-lg">
      <h2 className="section-title text-center mb-6">Login to Shujaa Studio</h2>
      <form onSubmit={handleSubmit}>
        {error && <p className="text-red-500 text-sm mb-4">{error}</p>}
        <div className="mb-4">
          <label htmlFor="username" className="block text-soft-text text-sm font-medium mb-2">Username</label>
          <input
            type="text"
            id="username"
            className="form-input w-full p-3 rounded-lg"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div className="mb-6">
          <label htmlFor="password" className="block text-soft-text text-sm font-medium mb-2">Password</label>
          <input
            type="password"
            id="password"
            className="form-input w-full p-3 rounded-lg"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button
          type="submit"
          className="btn-primary w-full py-3 rounded-lg text-white font-semibold flex items-center justify-center"
          disabled={isLoading}
        >
          {isLoading ? (
            <div className="loading-spinner mr-2"></div> // Conceptual spinner
          ) : (
            'Login'
          )}
        </button>
      </form>
      <p className="text-center text-soft-text text-sm mt-4">
        Don't have an account? <a href="/register" className="text-primary-gradient-start font-medium">Register here</a>
      </p>
    </div>
  );
};

export default LoginPage; // Export as default for page component