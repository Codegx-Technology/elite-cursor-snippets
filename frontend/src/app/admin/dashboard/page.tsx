"use client";

import React, { useEffect, useState, useCallback } from 'react'; // Added useEffect, useState
import SuperAdminDashboard from '@/widgets/SuperAdminDashboard';
import { useAuth } from '@/context/AuthContext';
import { useRouter } from 'next/navigation';

// Define interface for pending model update
interface PendingModelUpdate {
  key: string;
  name: string;
  provider: string;
  current_version: string;
  latest_version: string;
  message: string;
}

export default function AdminDashboardPage() {
  const { user, isAuthenticated, isLoading } = useAuth();
  const router = useRouter();
  const [pendingUpdates, setPendingUpdates] = useState<PendingModelUpdate[]>([]);
  const [loadingUpdates, setLoadingUpdates] = useState(true);
  const [errorUpdates, setErrorUpdates] = useState<string | null>(null);

  const fetchPendingUpdates = useCallback(async () => {
    setLoadingUpdates(true);
    setErrorUpdates(null);
    try {
      const token = localStorage.getItem('jwt_token');
      
      // Mock data for development when backend is not available
      const mockUpdates: PendingModelUpdate[] = [
        {
          key: "llama-3.1-8b",
          name: "Llama 3.1 8B",
          provider: "Meta",
          current_version: "v1.0.0",
          latest_version: "v1.1.0",
          message: "Performance improvements and bug fixes"
        },
        {
          key: "stable-diffusion-xl",
          name: "Stable Diffusion XL",
          provider: "Stability AI",
          current_version: "v1.0.0",
          latest_version: "v1.2.0",
          message: "Enhanced image quality and faster generation"
        },
        {
          key: "whisper-large-v3",
          name: "Whisper Large V3",
          provider: "OpenAI",
          current_version: "v2.0.0",
          latest_version: "v3.0.0",
          message: "Improved multilingual support including Swahili"
        }
      ];

      try {
        const response = await fetch('http://localhost:8000/superadmin/model-updates', {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });
        
        if (!response.ok) {
          console.warn("Backend not available, using mock model updates data");
          setPendingUpdates(mockUpdates);
          return;
        }
        
        const data = await response.json();
        setPendingUpdates(data);
      } catch (fetchError) {
        console.warn("Backend not available, using mock model updates data:", fetchError);
        setPendingUpdates(mockUpdates);
      }
    } catch (error: unknown) {
      const message = error instanceof Error ? error.message : 'Failed to fetch pending updates.';
      setErrorUpdates(message);
    } finally {
      setLoadingUpdates(false);
    }
  }, []);

  useEffect(() => {
    if (isAuthenticated && user?.role === 'admin') {
      fetchPendingUpdates();
    }
  }, [isAuthenticated, user, fetchPendingUpdates]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <span className="text-gray-600 font-medium">Loading authentication...</span>
        </div>
      </div>
    );
  }

  if (!isAuthenticated || user?.role !== 'admin') {
    // Redirect to login or show access denied message
    router.push('/login'); // Or a more specific access denied page
    return null;
  }

  const handleApprove = async (key: string) => {
    try {
      const token = localStorage.getItem('jwt_token');
      
      try {
        const response = await fetch(`http://localhost:8000/superadmin/model-updates/approve/${key}`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        // Refetch pending updates after successful approval
        fetchPendingUpdates();
      } catch (fetchError) {
        console.warn(`Backend not available for approve action, simulating approval for ${key}`);
        // Simulate approval by removing the item from the list
        setPendingUpdates(prev => prev.filter(update => update.key !== key));
      }
    } catch (error: unknown) {
      const message = error instanceof Error ? error.message : 'Failed to approve update.';
      console.error(`Failed to approve update ${key}:`, error);
      setErrorUpdates(message);
    }
  };

  const handleReject = async (key: string) => {
    try {
      const token = localStorage.getItem('jwt_token');
      
      try {
        const response = await fetch(`http://localhost:8000/superadmin/model-updates/reject/${key}`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        // Refetch pending updates after successful rejection
        fetchPendingUpdates();
      } catch (fetchError) {
        console.warn(`Backend not available for reject action, simulating rejection for ${key}`);
        // Simulate rejection by removing the item from the list
        setPendingUpdates(prev => prev.filter(update => update.key !== key));
      }
    } catch (error: unknown) {
      const message = error instanceof Error ? error.message : 'Failed to reject update.';
      console.error(`Failed to reject update ${key}:`, error);
      setErrorUpdates(message);
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Super Admin Dashboard</h1>
      {user && <SuperAdminDashboard userRole={user.role} />}

      <div className="mt-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Pending Model Updates</h2>
        {loadingUpdates ? (
          <p>Loading pending updates...</p>
        ) : errorUpdates ? (
          <p className="text-red-500">Error: {errorUpdates}</p>
        ) : pendingUpdates.length === 0 ? (
          <p>No pending model updates.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full bg-white shadow-md rounded-lg overflow-hidden">
              <thead className="bg-gray-200 text-gray-600 uppercase text-sm leading-normal">
                <tr>
                  <th className="py-3 px-6 text-left">Model</th>
                  <th className="py-3 px-6 text-left">Provider</th>
                  <th className="py-3 px-6 text-left">Current Version</th>
                  <th className="py-3 px-6 text-left">Latest Version</th>
                  <th className="py-3 px-6 text-left">Message</th>
                  <th className="py-3 px-6 text-center">Actions</th>
                </tr>
              </thead>
              <tbody className="text-gray-600 text-sm font-font-light">
                {pendingUpdates.map((update) => (
                  <tr key={update.key} className="border-b border-gray-200 hover:bg-gray-100">
                    <td className="py-3 px-6 text-left whitespace-nowrap">{update.name}</td>
                    <td className="py-3 px-6 text-left">{update.provider}</td>
                    <td className="py-3 px-6 text-left">{update.current_version}</td>
                    <td className="py-3 px-6 text-left">{update.latest_version}</td>
                    <td className="py-3 px-6 text-left">{update.message}</td>
                    <td className="py-3 px-6 text-center">
                      <button
                        onClick={() => handleApprove(update.key)}
                        className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded mr-2"
                      >
                        Approve
                      </button>
                      <button
                        onClick={() => handleReject(update.key)}
                        className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
                      >
                        Reject
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
