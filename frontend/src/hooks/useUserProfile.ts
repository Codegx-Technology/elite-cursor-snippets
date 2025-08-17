'use client';

import { useState, useEffect } from 'react';
import { apiClient, handleApiResponse } from '@/lib/api';

// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorclean
// [CONTEXT]: Custom hook for managing user profile state and logic
// [GOAL]: Encapsulate user profile complexity and provide a clean interface for UI components

export interface UserProfileData {
  username: string;
  email: string;
  full_name?: string;
  bio?: string;
}

export function useUserProfile() {
  const [profile, setProfile] = useState<UserProfileData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    setIsLoading(true);
    setError(null);
    const response = await apiClient.getProfile();
    handleApiResponse(
      response,
      (data) => setProfile(data),
      (error) => setError(error)
    );
    setIsLoading(false);
  };

  const updateProfile = async (data: Partial<UserProfileData>) => {
    setIsSaving(true);
    setError(null);
    setSuccessMessage(null);
    const response = await apiClient.updateProfile(data);
    handleApiResponse(
      response,
      (data) => {
        setProfile(data);
        setSuccessMessage('Profile updated successfully!');
      },
      (error) => setError(error)
    );
    setIsSaving(false);
  };

  return {
    profile,
    isLoading,
    isSaving,
    error,
    successMessage,
    loadProfile,
    updateProfile
  };
}