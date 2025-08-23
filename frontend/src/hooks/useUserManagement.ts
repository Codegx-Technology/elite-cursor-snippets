'use client';

import { useState, useEffect, useCallback } from 'react';
import { apiClient, handleApiResponse, CreateUserData } from '@/lib/api';

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

  const loadUsers = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await apiClient.getUsers();
      handleApiResponse(
        response,
        (data) => setUsers(data),
        (error) => setError(error)
      );
    } catch (e: unknown) {
      const message = e instanceof Error ? e.message : 'Failed to load users';
      setError(message);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const getUser = useCallback(async (id: number) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await apiClient.getUser(id);
      handleApiResponse(
        response,
        (data) => setUser(data),
        (error) => setError(error)
      );
    } catch (e: unknown) {
      const message = e instanceof Error ? e.message : 'Failed to load user';
      setError(message);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const createUser = useCallback(async (data: CreateUserData) => {
    try {
      const response = await apiClient.createUser(data);
      handleApiResponse(
        response,
        () => {
          loadUsers();
        },
        (error) => setError(error)
      );
    } catch (e: unknown) {
      const message = e instanceof Error ? e.message : 'Failed to create user';
      setError(message);
    }
  }, [loadUsers]);

  const updateUser = useCallback(async (id: number, data: Partial<UserData>) => {
    try {
      const response = await apiClient.updateUser(id, data);
      handleApiResponse(
        response,
        () => {
          loadUsers();
        },
        (error) => setError(error)
      );
    } catch (e: unknown) {
      const message = e instanceof Error ? e.message : 'Failed to update user';
      setError(message);
    }
  }, [loadUsers]);

  const deleteUser = useCallback(async (id: number) => {
    try {
      const response = await apiClient.deleteUser(id);
      handleApiResponse(
        response,
        () => {
          loadUsers();
        },
        (error) => setError(error)
      );
    } catch (e: unknown) {
      const message = e instanceof Error ? e.message : 'Failed to delete user';
      setError(message);
    }
  }, [loadUsers]);

  useEffect(() => {
    loadUsers();
  }, [loadUsers]);

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