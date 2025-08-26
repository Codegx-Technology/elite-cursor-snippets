// frontend/components/Dashboard/Dashboard.tsx (Conceptual)

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useRouter } from 'next/router';

interface UserProfile {
  username: string;
  email: string;
  // Add other profile fields as needed
}

interface UserPlan {
  plan_name: string;
  max_requests_per_day: number;
  cost_per_month: number;
  // Add other plan fields as needed
}

interface UserUsage {
  current_daily_usage: number;
  remaining_daily_usage: number;
  // Add other usage fields as needed
}

const Dashboard: React.FC = () => {
  const [userProfile, setUserProfile] = useState<UserProfile | null>(null);
  const [userPlan, setUserPlan] = useState<UserPlan | null>(null);
  const [userUsage, setUserUsage] = useState<UserUsage | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const getAuthHeaders = () => {
    const token = localStorage.getItem('jwt_token');
    if (!token) {
      router.push('/login');
      return {};
    }
    return { Authorization: `Bearer ${token}` };
  };

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const headers = getAuthHeaders();
        if (!headers.Authorization) return;

        // Fetch User Profile
        const profileResponse = await axios.get('http://localhost:8000/users/me', { headers });
        setUserProfile(profileResponse.data);

        // Fetch User Plan
        const planResponse = await axios.get('http://localhost:8000/users/me/plan', { headers });
        setUserPlan(planResponse.data);

        // Fetch User Usage
        const usageResponse = await axios.get('http://localhost:8000/users/me/usage', { headers });
        setUserUsage(usageResponse.data);

      } catch (err: unknown) {
        if ((err as any).response && (err as any).response.data && (err as any).response.data.detail) {
          setError((err as any).response.data.detail);
        } else {
          setError('Failed to load dashboard data. Please try again.');
        }
        console.error('Dashboard data fetch error:', err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  if (isLoading) {
    return (
      <div className="elite-container my-10 text-center">
        <div className="loading-spinner mx-auto mb-4"></div>
        <p className="text-soft-text">Loading dashboard...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="elite-container my-10 text-center text-red-500">
        <p>Error: {error}</p>
      </div>
    );
  }

  return (
    <div className="elite-container my-10">
      <h1 className="section-title text-center mb-8">Welcome, {userProfile?.username || 'User'}!</h1>

      <div className="responsive-grid mb-8">
        <div className="elite-card p-6">
          <h3 className="section-subtitle mb-2">Your Plan</h3>
          {userPlan ? (
            <>
              <p className="text-charcoal font-semibold text-lg">{userPlan.plan_name}</p>
              <p className="text-soft-text text-sm">Requests per day: {userPlan.max_requests_per_day}</p>
              <p className="text-soft-text text-sm">Cost per month: ${userPlan.cost_per_month}</p>
            </>
          ) : (
            <p className="text-soft-text">No plan information available.</p>
          )}
        </div>

        <div className="elite-card p-6">
          <h3 className="section-subtitle mb-2">Daily Usage</h3>
          {userUsage ? (
            <>
              <p className="text-charcoal font-semibold text-lg">Used: {userUsage.current_daily_usage}</p>
              <p className="text-soft-text text-sm">Remaining: {userUsage.remaining_daily_usage}</p>
            </>
          ) : (
            <p className="text-soft-text">No usage information available.</p>
          )}
        </div>

        {/* Add more cards for recent activities, quick links etc. */}
      </div>

      <div className="text-center mt-8">
        <button onClick={() => router.push('/generate')} className="btn-primary py-3 px-6 rounded-lg">
          Generate New Video
        </button>
      </div>
    </div>
  );
};

export default Dashboard;
