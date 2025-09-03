"use client";

import React, { useEffect, useState, useCallback } from 'react';
import { useAuth } from '@/context/AuthContext';
import { useRouter } from 'next/navigation';
import axios from 'axios';
import { DataTable } from '@/components/data-table/DataTable';
import { useToast } from '@/components/ui/use-toast';

interface TenantData {
  id: string;
  name: string;
  plan: string;
  users: string[];
}

interface ColumnDef<T> {
  accessorKey: keyof T;
  header: string | React.ReactNode;
  cell?: (row: T) => React.ReactNode;
  enableSorting?: boolean;
}

export default function TenantsPage() {
  const { user, isAuthenticated, isLoading, token } = useAuth();
  const router = useRouter();
  const [tenants, setTenants] = useState<TenantData[]>([]);
  const [loadingTenants, setLoadingTenants] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { addToast } = useToast();

  const fetchTenants = useCallback(async () => {
    setLoadingTenants(true);
    setError(null);
    try {
      const response = await axios.get('http://localhost:8000/admin/tenants', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setTenants(response.data.tenants);
    } catch (err: unknown) {
      console.warn('Backend not available, using mock tenants data:', err);
      // Mock data fallback for development
      const mockTenants: TenantData[] = [
        {
          id: '1',
          name: 'Shujaa HQ',
          plan: 'Enterprise',
          users: ['peter', 'apollo', 'admin1']
        },
        {
          id: '2',
          name: 'Example Corp',
          plan: 'Professional',
          users: ['jane_doe', 'user1']
        },
        {
          id: '3',
          name: 'Test Organization',
          plan: 'Free',
          users: ['test_user']
        }
      ];
      setTenants(mockTenants);
    } finally {
      setLoadingTenants(false);
    }
  }, [token, addToast]);

  useEffect(() => {
    if (!isLoading && (!isAuthenticated || user?.role !== 'admin')) {
      router.push('/login');
    } else if (isAuthenticated && user?.role === 'admin' && token) {
      fetchTenants();
    }
  }, [isLoading, isAuthenticated, user, router, token, fetchTenants]);

  if (isLoading || (!isAuthenticated && !loadingTenants)) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <span className="text-gray-600 font-medium">Loading...</span>
        </div>
      </div>
    );
  }

  const columns: ColumnDef<TenantData>[] = [
    { accessorKey: 'id', header: 'ID', enableSorting: true },
    { accessorKey: 'name', header: 'Name', enableSorting: true },
    { accessorKey: 'plan', header: 'Plan', enableSorting: true },
    {
      accessorKey: 'users',
      header: 'Users',
      cell: (row: TenantData) => row.users.join(', '),
    },
  ];

  return (
    <div className="space-y-6 p-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Tenant Management</h1>
      </div>

      {loadingTenants ? (
        <div className="text-center py-8">
          <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <span className="text-gray-600 font-medium">Loading tenants...</span>
        </div>
      ) : error ? (
        <div className="text-center py-8 text-red-500">{error}</div>
      ) : (
        <div className="overflow-x-auto rounded-lg shadow-md">
          <DataTable columns={columns} data={tenants} />
        </div>
      )}
    </div>
  );
}
