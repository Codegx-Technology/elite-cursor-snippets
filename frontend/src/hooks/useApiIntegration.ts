'use client';

import { useState, useEffect } from 'react';
import { apiClient, handleApiResponse } from '@/lib/api';

// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorclean
// [CONTEXT]: Custom hook for managing API keys and integrations
// [GOAL]: Encapsulate API integration complexity and provide a clean interface for UI components

export interface ApiKey {
  id: string;
  key: string;
  created_at: string;
  last_used_at?: string;
  is_active: boolean;
}

export interface Integration {
  id: string;
  name: string;
  type: string;
  is_enabled: boolean;
  config: Record<string, any>;
}

export function useApiIntegration() {
  const [apiKeys, setApiKeys] = useState<ApiKey[]>([]);
  const [integrations, setIntegrations] = useState<Integration[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadApiIntegrationData();
  }, []);

  const loadApiIntegrationData = async () => {
    setIsLoading(true);
    setError(null);
    const apiKeysResponse = await apiClient.getApiKeys();
    handleApiResponse(
      apiKeysResponse,
      (data) => setApiKeys(data),
      (error) => setError(error)
    );

    const integrationsResponse = await apiClient.getIntegrations();
    handleApiResponse(
      integrationsResponse,
      (data) => setIntegrations(data),
      (error) => setError(error)
    );
    setIsLoading(false);
  };

  const generateApiKey = async () => {
    const response = await apiClient.generateApiKey();
    handleApiResponse(
      response,
      () => {
        loadApiIntegrationData();
      },
      (error) => setError(error)
    );
  };

  const revokeApiKey = async (id: string) => {
    const response = await apiClient.revokeApiKey(id);
    handleApiResponse(
      response,
      () => {
        loadApiIntegrationData();
      },
      (error) => setError(error)
    );
  };

  const updateIntegration = async (id: string, config: Record<string, any>) => {
    const response = await apiClient.updateIntegration(id, config);
    handleApiResponse(
      response,
      () => {
        loadApiIntegrationData();
      },
      (error) => setError(error)
    );
  };

  return {
    apiKeys,
    integrations,
    isLoading,
    error,
    loadApiIntegrationData,
    generateApiKey,
    revokeApiKey,
    updateIntegration
  };
}
