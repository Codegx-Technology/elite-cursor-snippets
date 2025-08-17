'use client';

import { useState, useEffect } from 'react';
import { apiClient, handleApiResponse } from '@/lib/api';

// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorclean
// [CONTEXT]: Custom hook for managing usage analytics state and logic
// [GOAL]: Encapsulate usage analytics complexity and provide a clean interface for UI components

export interface UsageAnalyticsData {
  total_videos_generated: number;
  total_images_generated: number;
  total_audio_generated: number;
  daily_usage: {
    date: string;
    videos: number;
    images: number;
    audio: number;
  }[];
}

export function useUsageAnalytics() {
  const [analytics, setAnalytics] = useState<UsageAnalyticsData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadAnalytics();
  }, []);

  const loadAnalytics = async () => {
    setIsLoading(true);
    setError(null);
    const response = await apiClient.getUsageAnalytics();
    handleApiResponse(
      response,
      (data) => setAnalytics(data),
      (error) => setError(error)
    );
    setIsLoading(false);
  };

  return {
    analytics,
    isLoading,
    error,
    loadAnalytics
  };
}
