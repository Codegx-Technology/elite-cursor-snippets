'use client';

import { useState, useEffect } from 'react';
import { apiClient, handleApiResponse, AnalyticsData } from '@/lib/api';

// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorclean
// [CONTEXT]: Custom hook for managing usage analytics state and logic
// [GOAL]: Encapsulate usage analytics complexity and provide a clean interface for UI components

export function useUsageAnalytics() {
  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadAnalytics();
  }, []);

  const loadAnalytics = async () => {
    setIsLoading(true);
    setError(null);
    const response = await apiClient.getAnalytics();
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
