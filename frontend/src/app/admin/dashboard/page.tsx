"use client";

import React from 'react';
import SuperAdminDashboard from '@/widgets/SuperAdminDashboard'; // New import
import { useAuth } from '@/context/AuthContext';
import { useRouter } from 'next/navigation';

export default function AdminDashboardPage() {
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

  if (!isAuthenticated || user?.role !== 'admin') {
    // Redirect to login or show access denied message
    router.push('/login'); // Or a more specific access denied page
    return null;
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Super Admin Dashboard</h1>
      <SuperAdminDashboard userRole={user.role} />
    </div>
  );
}
