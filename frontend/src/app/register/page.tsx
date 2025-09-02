"use client";
import React, { useState } from 'react';
import { useRouter } from 'next/navigation'; // Use next/navigation for App Router
import Link from 'next/link';
import Layout from '@/components/Layout';

const RegisterPage: React.FC = () => { // Renamed to RegisterPage
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, email, password }),
      });

      if (!response.ok) {
        let detail = 'Registration failed';
        try { const errData = await response.json(); detail = errData?.detail ?? detail; } catch {}
        throw new Error(detail);
      }

      router.push('/login?registered=true'); // Redirect to login with success message

    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'An unexpected error occurred during registration. Please try again.';
      setError(message);
      console.error('Registration error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Layout>
      <div className="elite-card p-8 max-w-md mx-auto my-10 rounded-xl shadow-lg">
      {/* Back to Home Button */}
      <div className="mb-6">
        <Link
          href="/"
          className="inline-flex items-center text-sm text-gray-600 hover:text-green-600 transition-colors duration-200"
        >
          <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          Back to Home
        </Link>
      </div>

      <h2 className="section-title text-center mb-6">Register for Shujaa Studio</h2>
      <form onSubmit={handleSubmit}>
        {error && <p className="text-red-500 text-sm mb-4">{error}</p>}
        <div className="mb-4">
          <label htmlFor="reg-username" className="block text-soft-text text-sm font-medium mb-2">Username</label>
          <input
            type="text"
            id="reg-username"
            className="form-input w-full p-3 rounded-lg"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div className="mb-4">
          <label htmlFor="reg-email" className="block text-soft-text text-sm font-medium mb-2">Email</label>
          <input
            type="email"
            id="reg-email"
            className="form-input w-full p-3 rounded-lg"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div className="mb-6">
          <label htmlFor="reg-password" className="block text-soft-text text-sm font-medium mb-2">Password</label>
          <input
            type="password"
            id="reg-password"
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
            <div className="loading-spinner mr-2"></div>
          ) : (
            'Register'
          )}
        </button>
      </form>
      <p className="text-center text-soft-text text-sm mt-4">
        Already have an account? <Link href="/login" className="text-primary-gradient-start font-medium">Login here</Link>
      </p>
      </div>
    </Layout>
  );
};

export default RegisterPage; // Export as default for page component
