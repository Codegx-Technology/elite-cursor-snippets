'use client';

import React, { useState, useEffect } from 'react';
import { useAuth } from '@/context/AuthContext';
import { Card } from '@/components/ui/card';
import { FaChartLine, FaVideo, FaUsers, FaClock, FaDownload } from 'react-icons/fa6';
// Phase 2 Enterprise Components
import LoadingStates from '@/components/ui/LoadingStates';
import ErrorStates from '@/components/ui/ErrorStates';
import { BarChart, LineChart, DonutChart } from '@/components/charts/Chart';
import { apiClient } from '@/lib/api';

interface AnalyticsData {
  totalVideos: number;
  totalUsers: number;
  totalMinutes: number;
  monthlyGrowth: Array<{ label: string; value: number }>;
  contentTypes: Array<{ label: string; value: number; color?: string }>;
  regionalData: Array<{ label: string; value: number; color?: string }>;
}

export default function AnalyticsPage() {
  const { user, isLoading: authLoading } = useAuth();
  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAnalytics = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await apiClient.get('/analytics');
        const data = response.data;

        // Map backend data to frontend format
        const mappedData: AnalyticsData = {
          totalVideos: data.overview.total_videos,
          totalUsers: data.overview.total_users,
          totalMinutes: data.overview.total_videos * 1.5, // Placeholder calculation
          monthlyGrowth: data.usage_trends.map((item: { date: string | number; videos: number }) => ({
            label: new Date(item.date).toLocaleString('default', { month: 'short' }),
            value: item.videos,
          })),
          contentTypes: [
            { label: 'Videos 🎬', value: data.overview.total_videos, color: '#00A651' },
            { label: 'Images 🖼️', value: data.overview.total_images, color: '#FFD700' },
            { label: 'Audio 🎙️', value: data.overview.total_audio, color: '#3B82F6' },
          ],
          regionalData: [ // Keep mock data for this chart for now
            { label: 'Nairobi', value: 1250, color: '#00A651' },
            { label: 'Mombasa', value: 890, color: '#FFD700' },
            { label: 'Kisumu', value: 650, color: '#3B82F6' },
            { label: 'Nakuru', value: 420, color: '#8B5CF6' },
            { label: 'Eldoret', value: 380, color: '#F59E0B' }
          ]
        };

        setAnalytics(mappedData);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load analytics data.');
      } finally {
        setLoading(false);
      }
    };

    fetchAnalytics();
  }, []);

  if (authLoading || loading) {
    return (
      <div className="flex justify-center items-center min-h-screen-content">
        <LoadingStates.PageLoading message="Loading analytics... 🦁" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex justify-center items-center min-h-screen-content">
        <ErrorStates.ErrorPage 
          type="server-error"
          customTitle="Analytics Error"
          customMessage={error}
          onRetry={() => window.location.reload()}
        />
      </div>
    );
  }

  if (!analytics) {
    return (
      <div className="flex justify-center items-center min-h-screen-content">
        <ErrorStates.EmptyState 
          title="No Data Available"
          message="No analytics data found. 📊"
          icon={<FaChartLine className="text-5xl text-gray-300" />}
        />
      </div>
    );
  }

  return (
    <div className="container mx-auto p-4 sm:p-6 lg:p-8">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">
          Shujaa Studio Analytics 🇰🇪
        </h1>
        <p className="text-lg text-gray-600">Usage statistics and insights</p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <Card className="p-6 bg-gradient-to-br from-kenya-green/10 to-cultural-gold/10 border-kenya-green/20">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Videos</p>
              <p className="text-3xl font-bold text-gray-900">{analytics.totalVideos.toLocaleString()}</p>
              <p className="text-xs text-gray-500">Videos created</p>
            </div>
            <FaVideo className="text-4xl text-kenya-green" />
          </div>
        </Card>
        
        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Users</p>
              <p className="text-3xl font-bold text-gray-900">{analytics.totalUsers.toLocaleString()}</p>
              <p className="text-xs text-gray-500">Registered users</p>
            </div>
            <FaUsers className="text-4xl text-blue-600" />
          </div>
        </Card>
        
        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Video Minutes</p>
              <p className="text-3xl font-bold text-gray-900">{analytics.totalMinutes.toLocaleString()}</p>
              <p className="text-xs text-gray-500">Total content</p>
            </div>
            <FaClock className="text-4xl text-purple-600" />
          </div>
        </Card>
        
        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Growth</p>
              <p className="text-3xl font-bold text-gray-900">+23%</p>
              <p className="text-xs text-gray-500">This month</p>
            </div>
            <FaChartLine className="text-4xl text-teal-600" />
          </div>
        </Card>
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Monthly Growth */}
        <Card className="p-6">
          <h3 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
            <FaChartLine className="mr-2 text-kenya-green" /> Monthly Growth 🏃‍♂️
          </h3>
          <LineChart 
            data={analytics.monthlyGrowth}
            className="h-80"
            variant="kenya"
            title="Monthly Videos"
          />
        </Card>

        {/* Content Types */}
        <Card className="p-6">
          <h3 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
            <FaVideo className="mr-2 text-blue-600" /> Content Types 🎬
          </h3>
          <DonutChart 
            data={analytics.contentTypes}
            className="h-80"
            variant="cultural"
            title="Content Distribution"
          />
        </Card>
      </div>

      {/* Regional Data */}
      <Card className="p-6 mb-8">
        <h3 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
          <FaUsers className="mr-2 text-purple-600" /> Regional Data 🗺️
        </h3>
        <BarChart 
          data={analytics.regionalData}
          className="h-80"
          variant="kenya"
          title="Users by Region"
          showValues={true}
        />
      </Card>

      {/* Export Actions */}
      <div className="flex justify-end">
        <button className="flex items-center px-4 py-2 bg-kenya-green text-white rounded-lg hover:bg-kenya-green/90 transition-colors">
          <FaDownload className="mr-2" />
          Export Report 📄
        </button>
      </div>
    </div>
  );
}

