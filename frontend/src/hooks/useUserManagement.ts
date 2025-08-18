'use client';

import { useState, useEffect } from 'react';
import { apiClient, handleApiResponse } from '@/lib/api';

// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorclean
// [CONTEXT]: Custom hook for managing user management state and logic
// [GOAL]: Encapsulate user management complexity and provide a clean interface for UI components

export interface UserData {
  id: number;
  username: string;
  email: string;
  role: string;
  tenant_name: string;
  is_active: boolean;
}

export function useUserManagement() {
  const [users, setUsers] = useState<UserData[]>([]);
  const [user, setUser] = useState<UserData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

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

  const getUser = async (id: number) => {
    setIsLoading(true);
    setError(null);
    const response = await apiClient.getUser(id);
    handleApiResponse(
      response,
      (data) => setUser(data),
      (error) => setError(error)
    );
    setIsLoading(false);
  };

  const createUser = async (data: Omit<UserData, 'id'>) => {
    const response = await apiClient.createUser(data);
    handleApiResponse(
      response,
      () => {
        loadUsers();
      },
      (error) => setError(error)
    );
  };

  const updateUser = async (id: number, data: Partial<UserData>) => {
    const response = await apiClient.updateUser(id, data);
    handleApiResponse(
      response,
      () => {
        loadUsers();
      },
      (error) => setError(error)
    );
  };

  const deleteUser = async (id: number) => {
    const response = await apiClient.deleteUser(id);
    handleApiResponse(
      response,
      () => {
        loadUsers();
      },
      (error) => setError(error)
    );
  };

  // Ensure we load users when the hook mounts so UI doesn't get stuck in loading
  useEffect(() => {
    loadUsers();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return {
    users,
    user,
    isLoading,
    error,
    loadUsers,
    getUser,
    createUser,
    updateUser,
    deleteUser
  };
}