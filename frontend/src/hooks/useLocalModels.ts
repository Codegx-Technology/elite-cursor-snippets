'use client';

import { useState, useEffect } from 'react';
import { apiClient, handleApiResponse } from '@/lib/api';

// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorclean
// [CONTEXT]: Custom hook for managing local AI models
// [GOAL]: Encapsulate local model management complexity and provide a clean interface for UI components

export interface LocalModel {
  id: string;
  name: string;
  type: 'llm' | 'image_gen' | 'tts' | 'stt';
  version: string;
  size_gb: number;
  status: 'installed' | 'downloading' | 'available';
  download_progress?: number;
}

export function useLocalModels() {
  const [models, setModels] = useState<LocalModel[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadModels();
  }, []);

  const loadModels = async () => {
    setIsLoading(true);
    setError(null);
    const response = await apiClient.getLocalModels();
    handleApiResponse(
      response,
      (data) => setModels(data),
      (error) => setError(error)
    );
    setIsLoading(false);
  };

  const downloadModel = async (modelId: string) => {
    setModels((prev) =>
      prev.map((m) => (m.id === modelId ? { ...m, status: 'downloading', download_progress: 0 } : m))
    );
    const response = await apiClient.downloadLocalModel(modelId);
    handleApiResponse(
      response,
      () => {
        // In a real app, this would be handled by websockets or polling
        // For now, we'll just simulate the download progress
        let progress = 0;
        const interval = setInterval(() => {
          progress += 10;
          if (progress <= 100) {
            setModels((prev) =>
              prev.map((m) => (m.id === modelId ? { ...m, download_progress: progress } : m))
            );
          } else {
            clearInterval(interval);
            setModels((prev) =>
              prev.map((m) => (m.id === modelId ? { ...m, status: 'installed', download_progress: undefined } : m))
            );
          }
        }, 200);
      },
      (error) => {
        setError(error);
        setModels((prev) =>
          prev.map((m) => (m.id === modelId ? { ...m, status: 'available', download_progress: undefined } : m))
        );
      }
    );
  };

  const deleteModel = async (modelId: string) => {
    const response = await apiClient.deleteLocalModel(modelId);
    handleApiResponse(
      response,
      () => {
        setModels((prev) => prev.filter((m) => m.id !== modelId));
      },
      (error) => setError(error)
    );
  };

  return {
    models,
    isLoading,
    error,
    loadModels,
    downloadModel,
    deleteModel
  };
}