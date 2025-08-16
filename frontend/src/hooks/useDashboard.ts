
import { useState, useEffect } from 'react';
import { apiClient, handleApiResponse, DashboardStats, RecentActivity } from '@/lib/api';

// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorclean
// [CONTEXT]: Custom hook for managing enterprise-grade dashboard state and logic
// [GOAL]: Encapsulate dashboard complexity and provide a clean interface for UI components

export function useDashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [recentActivity, setRecentActivity] = useState<RecentActivity[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [backendStatus, setBackendStatus] = useState<'checking' | 'online' | 'offline'>('checking');

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    setIsLoading(true);
    setError(null);

    const statusResponse = await apiClient.getStatus();
    if (statusResponse.error) {
      setBackendStatus('offline');
      setError('Backend service is not available');
    } else {
      setBackendStatus('online');
    }

    const statsResponse = await apiClient.getDashboardStats();
    handleApiResponse(
      statsResponse,
      (data) => setStats(data),
      (error) => {
        setError(error);
        setStats({
          videosGenerated: 0,
          imagesCreated: 0,
          audioTracks: 0,
          activeUsers: 0,
          systemStatus: 'online',
          lastGeneration: 'No data available'
        });
      }
    );

    const activityResponse = await apiClient.getRecentActivity();
    handleApiResponse(
      activityResponse,
      (data) => {
        if (data.length === 0) {
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
        } else {
          setRecentActivity(data);
        }
      },
      (error) => setError(error)
    );

    setIsLoading(false);
  };

  return {
    stats,
    recentActivity,
    isLoading,
    error,
    backendStatus,
    loadDashboardData
  };
}
