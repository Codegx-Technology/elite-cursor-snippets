'use client';

import { useState, useEffect } from 'react';
import { apiClient, handleApiResponse } from '@/lib/api';

export interface TenantData {
  id: number;
  name: string;
  is_active: boolean;
  plan: string;
  # Add other tenant-specific fields as needed
}

export interface CreateTenantData {
  name: string;
  is_active?: boolean;
  plan?: string;
}

export function useTenantManagement() {
  const [tenants, setTenants] = useState<TenantData[]>([]);
  const [tenant, setTenant] = useState<TenantData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadTenants = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await apiClient.getTenants();
      handleApiResponse(
        response,
        (data) => setTenants(data),
        (error) => setError(error)
      );
    } catch (e: any) {
      setError(e?.message || 'Failed to load tenants');
    } finally {
      setIsLoading(false);
    }
  };

  const getTenant = async (id: number) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await apiClient.getTenant(id);
      handleApiResponse(
        response,
        (data) => setTenant(data),
        (error) => setError(error)
      );
    } catch (e: any) {
      setError(e?.message || 'Failed to load tenant');
    } finally {
      setIsLoading(false);
    }
  };

  const createTenant = async (data: CreateTenantData) => {
    try {
      const response = await apiClient.createTenant(data);
      handleApiResponse(
        response,
        () => {
          loadTenants();
        },
        (error) => setError(error)
      );
    } catch (e: any) {
      setError(e?.message || 'Failed to create tenant');
    }
  };

  const updateTenant = async (id: number, data: Partial<TenantData>) => {
    try {
      const response = await apiClient.updateTenant(id, data);
      handleApiResponse(
        response,
        () => {
          loadTenants();
        },
        (error) => setError(error)
      );
    } catch (e: any) {
      setError(e?.message || 'Failed to update tenant');
    }
  };

  const deleteTenant = async (id: number) => {
    try {
      const response = await apiClient.deleteTenant(id);
      handleApiResponse(
        response,
        () => {
          loadTenants();
        },
        (error) => setError(error)
      );
    } catch (e: any) {
      setError(e?.message || 'Failed to delete tenant');
    }
  };

  useEffect(() => {
    loadTenants();
  }, []);

  return {
    tenants,
    tenant,
    isLoading,
    error,
    loadTenants,
    getTenant,
    createTenant,
    updateTenant,
    deleteTenant
  };
}
