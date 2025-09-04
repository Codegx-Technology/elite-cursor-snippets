// frontend/src/widgets/SuperAdminDashboard/adminService.ts
// [TASK]: Admin service functions for SuperAdminDashboard
// [GOAL]: Provide API functions for user management, tenant management, and admin operations
// [SNIPPET]: surgicalfix + modulefix + kenyafirst
// [CONTEXT]: Following GEMINI.md contract and elite-cursor-snippets methodology

import type { UserData } from '@/lib/api';

// Base API URL - should match backend
const API_BASE_URL = 'http://localhost:8000';

// Helper function to get auth token
const getAuthToken = (): string | null => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('jwt_token');
  }
  return null;
};

// Helper function to make authenticated requests
const makeAuthenticatedRequest = async (endpoint: string, options: RequestInit = {}) => {
  const token = getAuthToken();
  
  if (!token) {
    throw new Error('No authentication token found. Please log in.');
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  if (!response.ok) {
    if (response.status === 401) {
      throw new Error('Authentication failed. Please log in again.');
    }
    throw new Error(`API request failed: ${response.status} ${response.statusText}`);
  }

  return response.json();
};

// User Management Functions
export const fetchAllUsers = async (): Promise<UserData[]> => {
  try {
    // For now, return mock data since we don't have a full user management API
    // In production, this would call: makeAuthenticatedRequest('/admin/users')
    
    const mockUsers: UserData[] = [
      {
        id: 1,
        username: 'peter',
        email: 'peter@shujaa.studio',
        role: 'admin',
        tenant_name: 'Shujaa Studio',
        is_active: true,
      },
      {
        id: 2,
        username: 'apollo',
        email: 'apollo@shujaa.studio',
        role: 'user',
        tenant_name: 'Shujaa Studio',
        is_active: true,
      },
    ];

    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 500));
    
    return mockUsers;
  } catch (error) {
    console.error('Error fetching users:', error);
    throw error;
  }
};

// Tenant Management Functions
export const fetchAllTenants = async () => {
  try {
    // Mock tenant data for now
    const mockTenants = [
      {
        id: 'tenant-1',
        name: 'Shujaa Studio',
        domain: 'shujaa.studio',
        plan: 'enterprise',
        users_count: 2,
        created_at: new Date().toISOString(),
        is_active: true,
      },
    ];

    await new Promise(resolve => setTimeout(resolve, 300));
    return mockTenants;
  } catch (error) {
    console.error('Error fetching tenants:', error);
    throw error;
  }
};

// Audit Log Functions
export const fetchAuditLogs = async () => {
  try {
    // Mock audit log data
    const mockLogs = [
      {
        id: 'log-1',
        user_id: 'user-1',
        action: 'login',
        resource: 'authentication',
        timestamp: new Date().toISOString(),
        ip_address: '127.0.0.1',
        user_agent: 'Mozilla/5.0...',
      },
      {
        id: 'log-2',
        user_id: 'user-2',
        action: 'video_generation',
        resource: 'video',
        timestamp: new Date(Date.now() - 3600000).toISOString(),
        ip_address: '127.0.0.1',
        user_agent: 'Mozilla/5.0...',
      },
    ];

    await new Promise(resolve => setTimeout(resolve, 400));
    return mockLogs;
  } catch (error) {
    console.error('Error fetching audit logs:', error);
    throw error;
  }
};

// TTS Voice Management Functions
export const fetchTTSVoices = async () => {
  try {
    // Mock TTS voice data
    const mockVoices = [
      {
        id: 'voice-1',
        name: 'Kenyan English Female',
        language: 'en-KE',
        gender: 'female',
        provider: 'bark',
        is_active: true,
        sample_url: '/samples/kenyan-female.mp3',
      },
      {
        id: 'voice-2',
        name: 'Swahili Male',
        language: 'sw-KE',
        gender: 'male', 
        provider: 'bark',
        is_active: true,
        sample_url: '/samples/swahili-male.mp3',
      },
    ];

    await new Promise(resolve => setTimeout(resolve, 350));
    return mockVoices;
  } catch (error) {
    console.error('Error fetching TTS voices:', error);
    throw error;
  }
};

// System Stats Functions
export const fetchSystemStats = async () => {
  try {
    // Mock system statistics
    const mockStats = {
      total_users: 2,
      active_users: 2,
      total_videos_generated: 15,
      total_storage_used: '2.5 GB',
      system_uptime: '5 days, 12 hours',
      api_requests_today: 127,
      error_rate: '0.2%',
    };

    await new Promise(resolve => setTimeout(resolve, 200));
    return mockStats;
  } catch (error) {
    console.error('Error fetching system stats:', error);
    throw error;
  }
};

// Export all functions for easy importing
export default {
  fetchAllUsers,
  fetchAllTenants,
  fetchAuditLogs,
  fetchTTSVoices,
  fetchSystemStats,
};
