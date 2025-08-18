'use client';

import { useState, useEffect } from 'react';
import { apiClient, handleApiResponse } from '@/lib/api';
import { UserData } from './useUserManagement';

// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorclean
// [CONTEXT]: Custom hook for managing RBAC state and logic
// [GOAL]: Encapsulate RBAC complexity and provide a clean interface for UI components

export function useRBAC() {
  const [users, setUsers] = useState<UserData[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadUsers();
  }, []);

  const loadUsers = async () => {
    setIsLoading(true);
    setError(null);
    const response = await apiClient.getUsers();
    handleApiResponse(
      response,
      (data) => setUsers(data),
      (error) => setError(error)
    );
    setIsLoading(false);
  };

  const updateUserRole = async (id: number, role: string) => {
    const response = await apiClient.updateUser(id, { role });
    handleApiResponse(
      response,
      () => {
        loadUsers();
      },
      (error) => setError(error)
    );
  };

  return {
    users,
    isLoading,
    error,
    loadUsers,
    updateUserRole
  };
}
