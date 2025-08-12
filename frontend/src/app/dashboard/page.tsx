'use client';

import { useState, useEffect } from 'react';
import Card from '@/components/Card';
import { FaVideo, FaImages, FaMusic, FaUsers, FaChartLine, FaClock, FaFlag, FaMountain, FaGlobe, FaHeart, FaPlay, FaArrowRight } from 'react-icons/fa';

// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorclean
// [CONTEXT]: Enterprise-grade dashboard with Kenya-first design and mobile-first approach
// [GOAL]: Create clean, responsive dashboard with cultural authenticity
// [TASK]: Implement dashboard with proper error handling and mobile responsiveness

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
    videosGenerated: 247,
    imagesCreated: 1834,
    audioTracks: 156,
    activeUsers: 23,
    systemStatus: 'online',
    lastGeneration: '2 minutes ago'
  });

  const [recentActivity, setRecentActivity] = useState<RecentActivity[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  // [SNIPPET]: kenyafirst + thinkwithai
  // [TASK]: Load dashboard data with Kenya-first sample content
  useEffect(() => {
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
          <div className="w-8 h-8 border-4 border-green-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <span className="text-gray-600 font-medium">Loading dashboard...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Kenya-First Hero Section */}
      <div className="bg-gradient-to-r from-green-600 via-red-600 to-black p-6 rounded-xl text-white shadow-lg">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <FaFlag className="text-3xl" />
            <div>
              <h1 className="text-2xl font-bold">Karibu Shujaa Studio! 🇰🇪</h1>
              <p className="text-green-100">Empowering African storytellers with AI-powered video generation</p>
            </div>
          </div>
          <div className="hidden md:block">
            <FaMountain className="text-4xl text-yellow-300" />
          </div>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">Videos Generated</p>
              <p className="text-2xl font-bold text-gray-800">{stats.videosGenerated}</p>
            </div>
            <FaVideo className="text-3xl text-blue-600" />
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">Images Created</p>
              <p className="text-2xl font-bold text-gray-800">{stats.imagesCreated}</p>
            </div>
            <FaImages className="text-3xl text-green-600" />
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">Audio Tracks</p>
              <p className="text-2xl font-bold text-gray-800">{stats.audioTracks}</p>
            </div>
            <FaMusic className="text-3xl text-purple-600" />
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">Active Users</p>
              <p className="text-2xl font-bold text-gray-800">{stats.activeUsers}</p>
            </div>
            <FaUsers className="text-3xl text-orange-600" />
          </div>
        </Card>
      </div>

      {/* Quick Actions */}
      <Card className="p-6">
        <h2 className="text-xl font-bold text-gray-800 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button className="bg-blue-600 hover:bg-blue-700 text-white p-4 rounded-lg transition-colors duration-200 flex items-center space-x-3">
            <FaVideo className="text-xl" />
            <div className="text-left">
              <h3 className="font-semibold">Generate Video</h3>
              <p className="text-sm opacity-90">Create Kenya-first content</p>
            </div>
          </button>

          <button className="bg-green-600 hover:bg-green-700 text-white p-4 rounded-lg transition-colors duration-200 flex items-center space-x-3">
            <FaImages className="text-xl" />
            <div className="text-left">
              <h3 className="font-semibold">Create Images</h3>
              <p className="text-sm opacity-90">Generate cultural imagery</p>
            </div>
          </button>

          <button className="bg-purple-600 hover:bg-purple-700 text-white p-4 rounded-lg transition-colors duration-200 flex items-center space-x-3">
            <FaMusic className="text-xl" />
            <div className="text-left">
              <h3 className="font-semibold">Audio Production</h3>
              <p className="text-sm opacity-90">Swahili narration</p>
            </div>
          </button>
        </div>
      </Card>

      {/* Cultural Footer */}
      <div className="bg-gradient-to-r from-yellow-400 via-red-500 to-green-600 p-6 rounded-lg text-white text-center">
        <div className="flex items-center justify-center space-x-2 mb-2">
          <FaGlobe className="text-xl" />
          <span className="font-bold">Proudly Kenyan</span>
          <FaHeart className="text-xl" />
        </div>
        <p className="text-sm">
          🌍 Serving African creators • 🎬 {stats.videosGenerated} videos celebrating heritage • 🇰🇪 Harambee spirit
        </p>
      </div>
    </div>
  );
}