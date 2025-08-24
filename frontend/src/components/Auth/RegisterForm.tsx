// frontend/components/Auth/RegisterForm.tsx (Conceptual)

import React, { useState } from 'react';
import axios from 'axios';
import { useRouter } from 'next/router';
import Link from 'next/link';

const RegisterForm: React.FC = () => {
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
      const response = await axios.post('http://localhost:8000/register', {
        username,
        email,
        password,
      });

      if (response.status === 200) {
        router.push('/login?registered=true'); // Redirect to login with success message
      }

    } catch (err: any) {
      if (err.response && err.response.data && err.response.data.detail) {
        setError(err.response.data.detail);
      } else {
        setError('An unexpected error occurred during registration. Please try again.');
      }
      console.error('Registration error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="elite-card p-8 max-w-md mx-auto my-10 rounded-xl shadow-lg">
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
  );
};

export default RegisterForm;