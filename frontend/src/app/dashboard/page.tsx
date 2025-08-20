'use client';

import Link from 'next/link';
import Card from '@/components/Card';
import { FaVideo, FaImages, FaMusic, FaUsers, FaClock, FaFlag, FaMountain, FaGlobe, FaHeart, FaExclamationTriangle } from 'react-icons/fa';
import { useDashboard } from '@/hooks/useDashboard';
import { useWidgetLoader } from '@/utils/widgetLoader'; // New import
import { usePlanGuard } from '@/context/PlanGuardContext'; // New import

// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorclean + augmentsearch
// [CONTEXT]: Enterprise-grade dashboard with Kenya-first design and real backend integration
// [GOAL]: Create clean, responsive dashboard with real data and proper error handling
// [TASK]: Implement dashboard with backend API integration and mobile responsiveness

export default function DashboardPage() {
  const { stats, recentActivity, backendStatus, loadDashboardData } = useDashboard(); // Removed isLoading and error
  const { planStatus, loading: planStatusLoading, error: planStatusError } = usePlanGuard(); // Get plan status from context

  // Load PlanGuardWidget and PlanGuardDashboardWidget using the loader
  const { component: PlanGuardWidgetComponent, allowed: planGuardWidgetAllowed, message: planGuardWidgetMessage } = useWidgetLoader("PlanGuardWidget", "test_user_id");
  const { component: PlanGuardDashboardWidgetComponent, allowed: planGuardDashboardWidgetAllowed, message: planGuardDashboardWidgetMessage } = useWidgetLoader("PlanGuardDashboardWidget", "test_user_id");

  const getActivityStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'bg-green-100 text-green-800';
      case 'processing': return 'bg-yellow-100 text-yellow-800';
      case 'failed': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getActivityIcon = (type: string) => {
    switch (type) {
      case 'video': return <FaVideo className="text-blue-600" aria-label="Video Icon" />;
      case 'image': return <FaImages className="text-green-600" aria-label="Image Icon" />;
      case 'audio': return <FaMusic className="text-purple-600" aria-label="Audio Icon" />;
      default: return <FaVideo className="text-gray-600" aria-label="Video Icon" />;
    }
  };

  if (planStatusLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="w-8 h-8 border-4 border-green-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <span className="text-gray-600 font-medium">Loading plan status...</span>
          <p className="text-sm text-gray-500 mt-2">Connecting to backend services...</p>
        </div>
      </div>
    );
  }

  if (planStatusError) {
    return (
      <Card className="p-8 text-center">
        <div className="text-red-600 mb-4">
          <FaExclamationTriangle className="text-4xl mx-auto mb-2" aria-label="Error Icon" />
          <p className="font-medium">Unable to load plan status</p>
          <p className="text-sm text-gray-600 mt-2">{planStatusError}</p>
        </div>
        <button
          onClick={loadDashboardData} // Still use this to try reloading dashboard data
          className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg transition-colors duration-200"
        >
          Try Again
        </button>
      </Card>
    );
  }

  const isRestricted = planStatus?.state === "view_only" || planStatus?.state === "locked";

  return (
    <div className="space-y-6">
      {/* PlanGuard Widget */}
      {planGuardWidgetAllowed ? (
        <PlanGuardWidgetComponent userId="test_user_id" isRestricted={isRestricted} />
      ) : (
        <Card className="p-4 text-center bg-yellow-50 border border-yellow-200">
          <p className="text-yellow-800">{planGuardWidgetMessage}</p>
        </Card>
      )}

      {/* PlanGuard Dashboard Widget */}
      {planGuardDashboardWidgetAllowed ? (
        <PlanGuardDashboardWidgetComponent userId="test_user_id" isRestricted={isRestricted} />
      ) : (
        <Card className="p-4 text-center bg-yellow-50 border border-yellow-200">
          <p className="text-yellow-800">{planGuardDashboardWidgetMessage}</p>
        </Card>
      )}

      {/* Kenya-First Hero Section */}
      <div className="bg-gradient-to-r from-green-600 via-red-600 to-black p-6 rounded-xl text-white shadow-lg">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <FaFlag className="text-3xl" aria-label="Kenyan Flag" />
            <div>
              <h1 className="text-2xl font-bold">Karibu Shujaa Studio! 🇰🇪</h1>
              <p className="text-green-100">Empowering African storytellers with AI-powered video generation</p>
              {backendStatus === 'offline' && (
                <div className="flex items-center space-x-2 mt-2 bg-red-500 bg-opacity-20 px-3 py-1 rounded">
                  <FaExclamationTriangle className="text-yellow-300 text-sm" aria-label="Warning Icon" />
                  <span className="text-yellow-100 text-sm">Backend service offline - showing sample data</span>
                </div>
              )}
            </div>
          </div>
          <div className="hidden md:block">
            <FaMountain className="text-4xl text-yellow-300" aria-label="Mount Kenya" />
          </div>
        </div>
      </div>

      {/* Stats Grid */}
      {error && !stats ? (
        <Card className="p-8 text-center">
          <div className="text-red-600 mb-4">
            <FaExclamationTriangle className="text-4xl mx-auto mb-2" aria-label="Error Icon" />
            <p className="font-medium">Unable to load dashboard data</p>
            <p className="text-sm text-gray-600 mt-2">{error}</p>
          </div>
          <button
            onClick={loadDashboardData}
            className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg transition-colors duration-200"
          >
            Try Again
          </button>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <Card className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm">Videos Generated</p>
                <p className="text-2xl font-bold text-gray-800">
                  {stats?.videosGenerated || 0}
                  {stats?.videosGenerated === 0 && (
                    <span className="text-sm text-gray-500 block">No data available</span>
                  )}
                </p>
              </div>
              <FaVideo className="text-3xl text-blue-600" aria-label="Video Icon" />
            </div>
          </Card>

          <Card className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm">Images Created</p>
                <p className="text-2xl font-bold text-gray-800">
                  {stats?.imagesCreated || 0}
                  {stats?.imagesCreated === 0 && (
                    <span className="text-sm text-gray-500 block">No data available</span>
                  )}
                </p>
              </div>
              <FaImages className="text-3xl text-green-600" aria-label="Image Icon" />
            </div>
          </Card>

          <Card className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm">Audio Tracks</p>
                <p className="text-2xl font-bold text-gray-800">
                  {stats?.audioTracks || 0}
                  {stats?.audioTracks === 0 && (
                    <span className="text-sm text-gray-500 block">No data available</span>
                  )}
                </p>
              </div>
              <FaMusic className="text-3xl text-purple-600" aria-label="Audio Icon" />
            </div>
          </Card>

          <Card className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm">Active Users</p>
                <p className="text-2xl font-bold text-gray-800">
                  {stats?.activeUsers || 0}
                  {stats?.activeUsers === 0 && (
                    <span className="text-sm text-gray-500 block">No data available</span>
                  )}
                </p>
              </div>
              <FaUsers className="text-3xl text-orange-600" aria-label="Users Icon" />
            </div>
          </Card>
        </div>
      )}

      {/* Quick Actions */}
      <Card className="p-6">
        <h2 className="text-xl font-bold text-gray-800 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Link href="/video-generate">
            <button className={`w-full bg-blue-600 hover:bg-blue-700 text-white p-4 rounded-lg transition-colors duration-200 flex items-center space-x-3 ${isRestricted ? 'opacity-50 cursor-not-allowed' : ''}`} disabled={isRestricted}>
              <FaVideo className="text-xl" aria-label="Video Icon" />
              <div className="text-left">
                <h3 className="font-semibold">Generate Video</h3>
                <p className="text-sm opacity-90">Create Kenya-first content</p>
              </div>
            </button>
          </Link>

          <Link href="/gallery">
            <button className={`w-full bg-green-600 hover:bg-green-700 text-white p-4 rounded-lg transition-colors duration-200 flex items-center space-x-3 ${isRestricted ? 'opacity-50 cursor-not-allowed' : ''}`} disabled={isRestricted}>
              <FaImages className="text-xl" aria-label="Image Icon" />
              <div className="text-left">
                <h3 className="font-semibold">Browse Gallery</h3>
                <p className="text-sm opacity-90">View generated content</p>
              </div>
            </button>
          </Link>

          <Link href="/audio-studio">
            <button className={`w-full bg-purple-600 hover:bg-purple-700 text-white p-4 rounded-lg transition-colors duration-200 flex items-center space-x-3 ${isRestricted ? 'opacity-50 cursor-not-allowed' : ''}`} disabled={isRestricted}>
              <FaMusic className="text-xl" aria-label="Audio Icon" />
              <div className="text-left">
                <h3 className="font-semibold">Audio Studio</h3>
                <p className="text-sm opacity-90">Voice & music creation</p>
              </div>
            </button>
          </Link>
        </div>
      </Card>

      {/* Recent Activity */}
      <Card className="p-6">
        <h2 className="text-xl font-bold text-gray-800 mb-4">Recent Activity</h2>
        {recentActivity.length === 0 ? (
          <div className="text-center py-8">
            <FaClock className="text-4xl text-gray-400 mx-auto mb-4" aria-label="Clock Icon" />
            <p className="text-gray-600 font-medium mb-2">No recent activity</p>
            <p className="text-sm text-gray-500">
              Start creating content to see your activity here.
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {recentActivity.map((activity) => (
              <div key={activity.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors duration-200">
                <div className="flex items-center space-x-3">
                  <div className="bg-white p-2 rounded-lg shadow-sm">
                    {getActivityIcon(activity.type)}
                  </div>
                  <div>
                    <p className="font-medium text-gray-800">{activity.title}</p>
                    <p className="text-sm text-gray-500">{activity.timestamp}</p>
                  </div>
                </div>
                <span className={`px-2 py-1 text-xs rounded-full font-medium ${getActivityStatusColor(activity.status)}`}>
                  {activity.status}
                </span>
              </div>
            ))}
          </div>
        )}
      </Card>

      {/* Cultural Footer */}
      <div className="bg-gradient-to-r from-yellow-400 via-red-500 to-green-600 p-6 rounded-lg text-white text-center">
        <div className="flex items-center justify-center space-x-2 mb-2">
          <FaGlobe className="text-xl" aria-label="Globe Icon" />
          <span className="font-bold">Proudly Kenyan</span>
          <FaHeart className="text-xl" aria-label="Heart Icon" />
        </div>
        <p className="text-sm">
          🌍 Serving African creators • 🎬 {stats?.videosGenerated || 0} videos celebrating heritage • 🇰🇪 Harambee spirit
        </p>
      </div>
    </div>
  );
}
