// frontend/components/Auth/LoginForm.tsx (Conceptual)

import React, { useState } from 'react';
import axios from 'axios'; // Assuming axios for API calls
import { useRouter } from 'next/router'; // Assuming Next.js router

const LoginForm: React.FC = () => {
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
      const response = await axios.post('http://localhost:8000/token', 
        new URLSearchParams({ username, password }), // Form URL-encoded data
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        }
      );

      const { access_token } = response.data;
      localStorage.setItem('jwt_token', access_token); // Store token securely
      router.push('/dashboard'); // Redirect to dashboard

    } catch (err: any) {
      if (err.response && err.response.data && err.response.data.detail) {
        setError(err.response.data.detail);
      } else {
        setError('An unexpected error occurred. Please try again.');
      }
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

export default LoginForm;