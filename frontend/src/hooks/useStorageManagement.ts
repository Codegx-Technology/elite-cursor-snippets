'use client';

import { useState, useEffect } from 'react';
import { apiClient, handleApiResponse } from '@/lib/api';

// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorclean
// [CONTEXT]: Custom hook for managing storage
// [GOAL]: Encapsulate storage management complexity and provide a clean interface for UI components

export interface StorageInfo {
  total_space_gb: number;
  used_space_gb: number;
  free_space_gb: number;
  cache_size_gb: number;
  project_data_size_gb: number;
  log_data_size_gb: number;
}

export function useStorageManagement() {
  const [storageInfo, setStorageInfo] = useState<StorageInfo | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadStorageInfo();
  }, []);

  const loadStorageInfo = async () => {
    setIsLoading(true);
    setError(null);
    const response = await apiClient.getStorageInfo();
    handleApiResponse(
      response,
      (data) => setStorageInfo(data),
      (error) => setError(error)
    );
    setIsLoading(false);
  };

  const clearCache = async () => {
    setIsLoading(true);
    setError(null);
    const response = await apiClient.clearCache();
    handleApiResponse(
      response,
      () => {
        loadStorageInfo();
      },
      (error) => setError(error)
    );
    setIsLoading(false);
  };

  return {
    storageInfo,
    isLoading,
    error,
    loadStorageInfo,
    clearCache
  };
}