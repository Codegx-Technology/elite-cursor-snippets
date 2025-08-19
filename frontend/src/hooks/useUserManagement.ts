'use client';

import { useState, useEffect } from 'react';
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

  const loadUsers = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await apiClient.getUsers();
      handleApiResponse(
        response,
        (data) => setUsers(data),
        (error) => setError(error)
      );
    } catch (e: any) {
      setError(e?.message || 'Failed to load users');
    } finally {
      setIsLoading(false);
    }
  };

  const getUser = async (id: number) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await apiClient.getUser(id);
      handleApiResponse(
        response,
        (data) => setUser(data),
        (error) => setError(error)
      );
    } catch (e: any) {
      setError(e?.message || 'Failed to load user');
    } finally {
      setIsLoading(false);
    }
  };

<<<<<<< HEAD
  const createUser = async (data: CreateUserData) => {
    try {
      const response = await apiClient.createUser(data);
      handleApiResponse(
        response,
        () => {
          loadUsers();
        },
        (error) => setError(error)
      );
    } catch (e: any) {
      setError(e?.message || 'Failed to create user');
    }
  };
=======
  const createUser = async (data: Omit<UserData, 'id'>) => {
    try {
      const response = await apiClient.createUser(data);
      handleApiResponse(
        response,
        () => {
          loadUsers();
        },
        (error) => setError(error)
      );
    } catch (e: any) {
      setError(e?.message || 'Failed to create user');
    }
>>>>>>> 9a6a59c61051fb013aec8064ee759dc0b89431b2
  };

  const updateUser = async (id: number, data: Partial<UserData>) => {
    try {
      const response = await apiClient.updateUser(id, data);
      handleApiResponse(
        response,
        () => {
          loadUsers();
        },
        (error) => setError(error)
      );
    } catch (e: any) {
      setError(e?.message || 'Failed to update user');
    }
  };

  const deleteUser = async (id: number) => {
    try {
      const response = await apiClient.deleteUser(id);
      handleApiResponse(
        response,
        () => {
          loadUsers();
        },
        (error) => setError(error)
      );
    } catch (e: any) {
      setError(e?.message || 'Failed to delete user');
    }
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