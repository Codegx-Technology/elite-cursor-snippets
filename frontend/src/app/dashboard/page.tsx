'use client';

import { useState, useEffect } from 'react';
import Card from '@/components/Card';
import { FaVideo, FaImages, FaMusic, FaUsers, FaChartLine, FaClock, FaFlag, FaMountain } from 'react-icons/fa';

// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorclean
// [CONTEXT]: Enterprise-grade dashboard with Kenya-first design and real-time capabilities
// [GOAL]: Create comprehensive dashboard showing video generation stats, system status, and cultural elements
// [TASK]: Implement dashboard with live data, Kenya-themed design, and enterprise features

interface DashboardStats {
  videosGenerated: number;
  imagesCreated: number;
  audioTracks: number;
  activeUsers: number;
  systemStatus: 'online' | 'offline' | 'maintenance';
  lastGeneration: string;
}

interface RecentActivity {
  id: string;
  type: 'video' | 'image' | 'audio';
  title: string;
  timestamp: string;
  status: 'completed' | 'processing' | 'failed';
}

export default function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats>({
    videosGenerated: 0,
    imagesCreated: 0,
    audioTracks: 0,
    activeUsers: 0,
    systemStatus: 'online',
    lastGeneration: 'Never'
  });

  const [recentActivity, setRecentActivity] = useState<RecentActivity[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // [SNIPPET]: kenyafirst + thinkwithai
  // [TASK]: Load dashboard data with Kenya-first sample content
  useEffect(() => {
    const loadDashboardData = async () => {
      try {
        // Simulate API call - in production, this would call the FastAPI backend
        await new Promise(resolve => setTimeout(resolve, 1000));

        setStats({
          videosGenerated: 247,
          imagesCreated: 1834,
          audioTracks: 156,
          activeUsers: 23,
          systemStatus: 'online',
          lastGeneration: '2 minutes ago'
        });

        setRecentActivity([
          {
            id: '1',
            type: 'video',
            title: 'Kenya Tourism: Mount Kenya Adventure',
            timestamp: '2 minutes ago',
            status: 'completed'
          },
          {
            id: '2',
            type: 'video',
            title: 'Nairobi Tech Hub Innovation Story',
            timestamp: '15 minutes ago',
            status: 'completed'
          },
          {
            id: '3',
            type: 'image',
            title: 'Maasai Mara Wildlife Scene',
            timestamp: '1 hour ago',
            status: 'processing'
          },
          {
            id: '4',
            type: 'audio',
            title: 'Swahili Narration: Coastal Beauty',
            timestamp: '2 hours ago',
            status: 'completed'
          }
        ]);

        setIsLoading(false);
      } catch (error) {
        console.error('Failed to load dashboard data:', error);
        setIsLoading(false);
      }
    };

    loadDashboardData();
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'online': return 'text-green-600';
      case 'offline': return 'text-red-600';
      case 'maintenance': return 'text-yellow-600';
      default: return 'text-gray-600';
    }
  };

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
      case 'video': return <FaVideo className="text-blue-600" />;
      case 'image': return <FaImages className="text-green-600" />;
      case 'audio': return <FaMusic className="text-purple-600" />;
      default: return <FaVideo className="text-gray-600" />;
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="loading-spinner"></div>
        <span className="ml-3 text-soft-text">Loading dashboard...</span>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Kenya-First Hero Section */}
      <div className="bg-gradient-to-r from-green-600 via-red-600 to-black p-6 rounded-xl text-white">
        <div className="flex items-center space-x-4">
          <FaFlag className="text-3xl" />
          <div>
            <h1 className="text-2xl font-bold">Karibu Shujaa Studio! 🇰🇪</h1>
            <p className="text-green-100">Empowering African storytellers with AI-powered video generation</p>
          </div>
          <div className="ml-auto">
            <FaMountain className="text-4xl text-yellow-300" />
          </div>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card className="p-6 hover-lift">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-soft-text text-sm">Videos Generated</p>
              <p className="text-2xl font-bold text-charcoal-text">{stats.videosGenerated}</p>
            </div>
            <FaVideo className="text-3xl text-blue-600" />
          </div>
        </Card>

        <Card className="p-6 hover-lift">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-soft-text text-sm">Images Created</p>
              <p className="text-2xl font-bold text-charcoal-text">{stats.imagesCreated}</p>
            </div>
            <FaImages className="text-3xl text-green-600" />
          </div>
        </Card>

        <Card className="p-6 hover-lift">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-soft-text text-sm">Audio Tracks</p>
              <p className="text-2xl font-bold text-charcoal-text">{stats.audioTracks}</p>
            </div>
            <FaMusic className="text-3xl text-purple-600" />
          </div>
        </Card>

        <Card className="p-6 hover-lift">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-soft-text text-sm">Active Users</p>
              <p className="text-2xl font-bold text-charcoal-text">{stats.activeUsers}</p>
            </div>
            <FaUsers className="text-3xl text-orange-600" />
          </div>
        </Card>
      </div>

      {/* System Status and Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* System Status */}
        <Card className="p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="section-title">System Status</h2>
            <div className={`flex items-center space-x-2 ${getStatusColor(stats.systemStatus)}`}>
              <div className="w-3 h-3 rounded-full bg-current"></div>
              <span className="font-medium capitalize">{stats.systemStatus}</span>
            </div>
          </div>

          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-soft-text">API Status</span>
              <span className="text-green-600 font-medium">Operational</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-soft-text">Model Loading</span>
              <span className="text-green-600 font-medium">Ready</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-soft-text">Storage</span>
              <span className="text-green-600 font-medium">85% Available</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-soft-text">Last Generation</span>
              <span className="text-charcoal-text font-medium">{stats.lastGeneration}</span>
            </div>
          </div>

          <div className="mt-6 p-4 bg-green-50 rounded-lg border border-green-200">
            <div className="flex items-center space-x-2">
              <FaChartLine className="text-green-600" />
              <span className="text-green-800 font-medium">All systems operational</span>
            </div>
            <p className="text-green-700 text-sm mt-1">
              Shujaa Studio is running smoothly. Ready to create amazing Kenya-first content!
            </p>
          </div>
        </Card>

        {/* Recent Activity */}
        <Card className="p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="section-title">Recent Activity</h2>
            <FaClock className="text-soft-text" />
          </div>

          <div className="space-y-4">
            {recentActivity.map((activity) => (
              <div key={activity.id} className="flex items-center space-x-4 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                <div className="flex-shrink-0">
                  {getActivityIcon(activity.type)}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-charcoal-text truncate">
                    {activity.title}
                  </p>
                  <p className="text-xs text-soft-text">{activity.timestamp}</p>
                </div>
                <div className="flex-shrink-0">
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getActivityStatusColor(activity.status)}`}>
                    {activity.status}
                  </span>
                </div>
              </div>
            ))}
          </div>

          <div className="mt-4 text-center">
            <button className="text-blue-600 hover:text-blue-800 text-sm font-medium">
              View all activity →
            </button>
          </div>
        </Card>
      </div>

      {/* Quick Actions */}
      <Card className="p-6">
        <h2 className="section-title mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button className="btn-primary p-4 text-left rounded-lg hover-lift">
            <FaVideo className="text-xl mb-2" />
            <div>
              <h3 className="font-semibold">Generate Video</h3>
              <p className="text-sm opacity-90">Create a new Kenya-first video</p>
            </div>
          </button>

          <button className="btn-elite p-4 text-left rounded-lg hover-lift text-white">
            <FaImages className="text-xl mb-2" />
            <div>
              <h3 className="font-semibold">Create Images</h3>
              <p className="text-sm opacity-90">Generate cultural imagery</p>
            </div>
          </button>

          <button className="bg-gradient-to-r from-green-600 to-green-700 text-white p-4 text-left rounded-lg hover-lift">
            <FaMusic className="text-xl mb-2" />
            <div>
              <h3 className="font-semibold">Audio Production</h3>
              <p className="text-sm opacity-90">Swahili narration & music</p>
            </div>
          </button>
        </div>
      </Card>

      {/* Kenya-First Cultural Footer */}
      <div className="bg-gradient-to-r from-yellow-400 via-red-500 to-green-600 p-4 rounded-lg text-white text-center">
        <p className="font-medium">
          🌍 Proudly serving African creators | 🎬 {stats.videosGenerated} videos celebrating our heritage |
          🇰🇪 Harambee spirit in every creation
        </p>
      </div>
    </div>
  );
}