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
        <div className="text-center">
          <div className="relative mb-4">
            <div className="w-16 h-16 border-4 border-transparent border-t-green-600 rounded-full animate-spin mx-auto"></div>
            <div className="absolute top-2 left-1/2 transform -translate-x-1/2 w-8 h-8 border-2 border-transparent border-t-red-500 rounded-full animate-spin"
                 style={{ animationDirection: 'reverse', animationDuration: '0.8s' }}></div>
            <div className="absolute inset-0 flex items-center justify-center">
              <FaFlag className="text-yellow-500 animate-pulse" />
            </div>
          </div>
          <span className="text-gray-600 font-medium">Loading your Kenya-first dashboard...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Kenya-First Hero Section */}
      <div className="relative overflow-hidden rounded-2xl shadow-2xl">
        <div
          className="p-8 text-white relative z-10"
          style={{
            background: 'linear-gradient(135deg, #00A651 0%, #FF6B35 50%, #000000 100%)'
          }}
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-6">
              <div className="flex items-center space-x-2">
                <FaFlag className="text-4xl animate-pulse" />
                <FaMountain className="text-4xl text-yellow-300 animate-float" />
              </div>
              <div>
                <h1 className="text-3xl font-bold mb-2">Karibu Shujaa Studio! 🇰🇪</h1>
                <p className="text-green-100 text-lg">Empowering African storytellers with AI-powered video generation</p>
                <p className="text-yellow-200 text-sm mt-1">Harambee spirit • Innovation • Cultural authenticity</p>
              </div>
            </div>
            <div className="hidden md:flex items-center space-x-4">
              <div className="text-right">
                <div className="text-2xl font-bold">{stats.videosGenerated}</div>
                <div className="text-green-200 text-sm">Videos Created</div>
              </div>
              <div className="w-px h-12 bg-white opacity-30"></div>
              <div className="text-right">
                <div className="text-2xl font-bold">{stats.activeUsers}</div>
                <div className="text-yellow-200 text-sm">Active Creators</div>
              </div>
            </div>
          </div>
        </div>

        {/* Decorative elements */}
        <div className="absolute top-0 right-0 w-32 h-32 bg-yellow-400 rounded-full opacity-10 -translate-y-16 translate-x-16"></div>
        <div className="absolute bottom-0 left-0 w-24 h-24 bg-green-400 rounded-full opacity-10 translate-y-12 -translate-x-12"></div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card variant="elite" padding="md" className="group">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm font-medium">Videos Generated</p>
              <p className="text-3xl font-bold text-gray-800 mt-1">{stats.videosGenerated}</p>
              <p className="text-green-600 text-xs mt-1 flex items-center">
                <span className="w-2 h-2 bg-green-500 rounded-full mr-1"></span>
                +12% this week
              </p>
            </div>
            <div className="p-3 bg-blue-100 rounded-xl group-hover:bg-blue-200 transition-colors duration-200">
              <FaVideo className="text-2xl text-blue-600" />
            </div>
          </div>
        </Card>

        <Card variant="elite" padding="md" className="group">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm font-medium">Images Created</p>
              <p className="text-3xl font-bold text-gray-800 mt-1">{stats.imagesCreated}</p>
              <p className="text-green-600 text-xs mt-1 flex items-center">
                <span className="w-2 h-2 bg-green-500 rounded-full mr-1"></span>
                +8% this week
              </p>
            </div>
            <div className="p-3 bg-green-100 rounded-xl group-hover:bg-green-200 transition-colors duration-200">
              <FaImages className="text-2xl text-green-600" />
            </div>
          </div>
        </Card>

        <Card variant="elite" padding="md" className="group">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm font-medium">Audio Tracks</p>
              <p className="text-3xl font-bold text-gray-800 mt-1">{stats.audioTracks}</p>
              <p className="text-green-600 text-xs mt-1 flex items-center">
                <span className="w-2 h-2 bg-green-500 rounded-full mr-1"></span>
                +15% this week
              </p>
            </div>
            <div className="p-3 bg-purple-100 rounded-xl group-hover:bg-purple-200 transition-colors duration-200">
              <FaMusic className="text-2xl text-purple-600" />
            </div>
          </div>
        </Card>

        <Card variant="elite" padding="md" className="group">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm font-medium">Active Users</p>
              <p className="text-3xl font-bold text-gray-800 mt-1">{stats.activeUsers}</p>
              <p className="text-green-600 text-xs mt-1 flex items-center">
                <span className="w-2 h-2 bg-green-500 rounded-full mr-1"></span>
                +5% this week
              </p>
            </div>
            <div className="p-3 bg-orange-100 rounded-xl group-hover:bg-orange-200 transition-colors duration-200">
              <FaUsers className="text-2xl text-orange-600" />
            </div>
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
      <Card variant="elite" padding="lg">
        <h2 className="section-title mb-6 text-gradient-kenya">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <button className="group relative overflow-hidden bg-gradient-to-br from-blue-500 to-blue-600 text-white p-6 rounded-2xl hover:from-blue-600 hover:to-blue-700 transition-all duration-300 transform hover:scale-105 hover:shadow-2xl">
            <div className="relative z-10">
              <div className="flex items-center justify-between mb-4">
                <FaVideo className="text-3xl" />
                <div className="w-8 h-8 bg-white bg-opacity-20 rounded-full flex items-center justify-center">
                  <span className="text-xs font-bold">🎬</span>
                </div>
              </div>
              <h3 className="font-bold text-lg mb-2">Generate Video</h3>
              <p className="text-blue-100 text-sm">Create stunning Kenya-first videos with AI</p>
            </div>
            <div className="absolute top-0 right-0 w-20 h-20 bg-white opacity-5 rounded-full -translate-y-10 translate-x-10 group-hover:scale-150 transition-transform duration-500"></div>
          </button>

          <button className="group relative overflow-hidden bg-gradient-to-br from-green-500 to-green-600 text-white p-6 rounded-2xl hover:from-green-600 hover:to-green-700 transition-all duration-300 transform hover:scale-105 hover:shadow-2xl">
            <div className="relative z-10">
              <div className="flex items-center justify-between mb-4">
                <FaImages className="text-3xl" />
                <div className="w-8 h-8 bg-white bg-opacity-20 rounded-full flex items-center justify-center">
                  <span className="text-xs font-bold">🖼️</span>
                </div>
              </div>
              <h3 className="font-bold text-lg mb-2">Create Images</h3>
              <p className="text-green-100 text-sm">Generate beautiful cultural imagery</p>
            </div>
            <div className="absolute top-0 right-0 w-20 h-20 bg-white opacity-5 rounded-full -translate-y-10 translate-x-10 group-hover:scale-150 transition-transform duration-500"></div>
          </button>

          <button className="group relative overflow-hidden bg-gradient-to-br from-purple-500 to-purple-600 text-white p-6 rounded-2xl hover:from-purple-600 hover:to-purple-700 transition-all duration-300 transform hover:scale-105 hover:shadow-2xl">
            <div className="relative z-10">
              <div className="flex items-center justify-between mb-4">
                <FaMusic className="text-3xl" />
                <div className="w-8 h-8 bg-white bg-opacity-20 rounded-full flex items-center justify-center">
                  <span className="text-xs font-bold">🎵</span>
                </div>
              </div>
              <h3 className="font-bold text-lg mb-2">Audio Production</h3>
              <p className="text-purple-100 text-sm">Swahili narration & traditional music</p>
            </div>
            <div className="absolute top-0 right-0 w-20 h-20 bg-white opacity-5 rounded-full -translate-y-10 translate-x-10 group-hover:scale-150 transition-transform duration-500"></div>
          </button>
        </div>
      </Card>

      {/* Kenya-First Cultural Footer */}
      <div className="relative overflow-hidden rounded-2xl shadow-xl">
        <div
          className="p-8 text-white text-center relative z-10"
          style={{
            background: 'linear-gradient(135deg, #FFD700 0%, #FF6B35 50%, #00A651 100%)'
          }}
        >
          <div className="flex items-center justify-center space-x-2 mb-4">
            <FaGlobe className="text-2xl animate-pulse" />
            <span className="text-xl font-bold">Proudly Kenyan</span>
            <FaHeart className="text-2xl text-red-300 animate-pulse" />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
            <div className="flex items-center justify-center space-x-2">
              <span className="text-2xl">🌍</span>
              <span>Serving African creators worldwide</span>
            </div>
            <div className="flex items-center justify-center space-x-2">
              <span className="text-2xl">🎬</span>
              <span>{stats.videosGenerated} videos celebrating our heritage</span>
            </div>
            <div className="flex items-center justify-center space-x-2">
              <span className="text-2xl">🇰🇪</span>
              <span>Harambee spirit in every creation</span>
            </div>
          </div>

          <div className="mt-4 text-xs opacity-90">
            "Ubuntu: I am because we are" • Made with ❤️ in Kenya
          </div>
        </div>

        {/* Decorative elements */}
        <div className="absolute top-0 left-0 w-16 h-16 bg-white opacity-10 rounded-full -translate-y-8 -translate-x-8"></div>
        <div className="absolute bottom-0 right-0 w-12 h-12 bg-white opacity-10 rounded-full translate-y-6 translate-x-6"></div>
      </div>
    </div>
  );
}