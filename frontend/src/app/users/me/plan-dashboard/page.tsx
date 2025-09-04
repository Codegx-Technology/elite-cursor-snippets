// frontend/src/app/users/me/plan-dashboard/page.tsx

"use client";

import React from 'react';
import UserPlanDashboardWidget from '@/widgets/UserPlanDashboard';
import { useAuth } from '@/context/AuthContext';
import { useRouter } from 'next/navigation';

export default function UserPlanDashboardPage() {
  const { user, isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <span className="text-gray-600 font-medium">Loading authentication...</span>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    router.push('/login');
    return null;
  }

  return (
    <div className="space-y-6">
      <UserPlanDashboardWidget />
    </div>
  );
}
