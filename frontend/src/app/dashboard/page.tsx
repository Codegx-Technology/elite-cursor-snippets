// [TASK]: Create a new page component for the user dashboard.
// [GOAL]: Provide a central hub for users to view PlanGuard info, recent projects, and account settings.
// [CONSTRAINTS]: Integrate seamlessly with existing UI, use Tailwind CSS, apply Kenya-first principles.
// [SNIPPET]: thinkwithai + kenyafirst + refactorclean + taskchain
// [CONTEXT]: Building out the enterprise-grade UI, starting with the user dashboard.

"use client";

import React from 'react';
import { usePlanGuard } from '@/context/PlanGuardContext';
import { useAuth } from '@/context/AuthContext';
import Link from 'next/link';
import { FaVideo, FaCreditCard, FaCog, FaChartLine } from 'react-icons/fa';

// [SNIPPET]: thinkwithai + kenyafirst + refactorclean
// [CONTEXT]: Dashboard page component for Shujaa Studio users.
// [GOAL]: Display user-specific information like plan status, usage, and quick links.
// [TASK]: Implement the main dashboard layout and integrate data from contexts.

export default function DashboardPage() {
  const { planStatus, loading: planLoading, error: planError } = usePlanGuard();
  const { user, isLoading: authLoading } = useAuth();

  if (planLoading || authLoading) {
    return (
      <div className="flex justify-center items-center min-h-screen-content">
        <p className="text-gray-600">Loading dashboard data...</p>
      </div>
    );
  }

  if (planError) {
    return (
      <div className="flex justify-center items-center min-h-screen-content">
        <p className="text-red-600">Error loading plan information: {planError}</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-4 sm:p-6 lg:p-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">
        Welcome, {user?.username || 'Shujaa'}!
      </h1>

      {/* PlanGuard Overview */}
      <section className="bg-white shadow-lg rounded-lg p-6 mb-8">
        <h2 className="text-2xl font-semibold text-gray-800 mb-4 flex items-center">
          <FaCreditCard className="mr-3 text-green-600" /> Your Plan Overview
        </h2>
        {planStatus ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <p className="text-gray-700 text-lg">
                Current Plan: <span className="font-bold text-green-700">{planStatus.planName}</span>
              </p>
              <p className="text-gray-600">
                Status: <span className="font-medium">{planStatus.state}</span>
              </p>
              <p className="text-gray-600">
                Expires: <span className="font-medium">{planStatus.expiresAt ? new Date(planStatus.expiresAt).toLocaleDateString() : 'N/A'}</span>
              </p>
            </div>
            <div>
              <p className="text-gray-700 text-lg">
                Video Minutes Used: <span className="font-bold">{planStatus.usage.videoMins} / {planStatus.quota.videoMins}</span>
              </p>
              <Link href="/pricing" className="text-blue-600 hover:underline mt-2 inline-block">
                Upgrade Your Plan
              </Link>
            </div>
          </div>
        ) : (
          <p className="text-gray-600">No plan information available. Please check your subscription.</p>
        )}
      </section>

      {/* Recent Projects (Placeholder) */}
      <section className="bg-white shadow-lg rounded-lg p-6 mb-8">
        <h2 className="text-2xl font-semibold text-gray-800 mb-4 flex items-center">
          <FaVideo className="mr-3 text-blue-600" /> Your Recent Projects
        </h2>
        <p className="text-gray-600 mb-4">
          This section will display your recently generated videos and projects.
          <br />
          <Link href="/projects" className="text-blue-600 hover:underline mt-2 inline-block">
            View All Projects
          </Link>
        </p>
        {/* TODO: Implement fetching and displaying actual recent projects */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {/* Placeholder for project cards */}
          <div className="border border-gray-200 rounded-lg p-4 text-center">
            <FaVideo className="text-5xl text-gray-300 mx-auto mb-3" />
            <p className="text-gray-500">No recent projects yet.</p>
            <Link href="/video-generate" className="text-green-600 hover:underline mt-2 inline-block">
              Start Creating Now!
            </Link>
          </div>
        </div>
      </section>

      {/* Quick Links */}
      <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div className="bg-white shadow-lg rounded-lg p-6 flex flex-col items-center text-center">
          <FaCog className="text-5xl text-purple-600 mb-4" />
          <h3 className="text-xl font-semibold text-gray-800 mb-2">Account Settings</h3>
          <p className="text-gray-600 mb-4">Manage your profile, security, and preferences.</p>
          <Link href="/profile" className="btn-primary">
            Go to Settings
          </Link>
        </div>

        <div className="bg-white shadow-lg rounded-lg p-6 flex flex-col items-center text-center">
          <FaChartLine className="text-5xl text-teal-600 mb-4" />
          <h3 className="text-xl font-semibold text-gray-800 mb-2">Usage & Analytics</h3>
          <p className="text-gray-600 mb-4">Monitor your resource consumption and performance.</p>
          <Link href="/usage" className="btn-primary">
            View Analytics
          </Link>
        </div>

        <div className="bg-white shadow-lg rounded-lg p-6 flex flex-col items-center text-center">
          <FaVideo className="text-5xl text-orange-600 mb-4" />
          <h3 className="text-xl font-semibold text-gray-800 mb-2">Start New Video</h3>
          <p className="text-gray-600 mb-4">Jump directly into creating your next masterpiece.</p>
          <Link href="/video-generate" className="btn-primary">
            Create Video
          </Link>
        </div>
      </section>
    </div>
  );
}