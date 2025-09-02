"use client";

import React, { useEffect, useState, useCallback } from 'react';
import { useAuth } from '@/context/AuthContext';
import { useRouter } from 'next/navigation';
import axios from 'axios';
import { Button } from '@/components/ui/button';
import { useToast } from '@/components/ui/use-toast';
import { FaPencilAlt, FaPlus, FaTrashCan } from 'react-icons/fa6';
import { DataTable } from '@/components/data-table/DataTable';

interface UserData {
  id: string;
  username: string;
  email: string;
  role: string;
  tenant_name: string;
  is_active: boolean;
}

interface ColumnDef<T> {
  accessorKey: keyof T;
  header: string | React.ReactNode;
  cell?: (row: T) => React.ReactNode;
  enableSorting?: boolean;
}

export default function AdminUsersPage() {
  const { user, isAuthenticated, isLoading, token } = useAuth();
  const router = useRouter();
  const [users, setUsers] = useState<UserData[]>([]);
  const [loadingUsers, setLoadingUsers] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { addToast } = useToast();

  const fetchUsers = useCallback(async () => {
    setLoadingUsers(true);
    setError(null);
    try {
      const response = await axios.get('http://localhost:8000/api/users', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setUsers(response.data);
    } catch (err: unknown) {
      console.error('Failed to fetch users:', err);
      const message = axios.isAxiosError(err) && err.response?.data?.detail ? err.response.data.detail : 'Failed to fetch users.';
      setError(message);
      addToast({
        title: "Error",
        description: message,
        type: "error",
      });
    } finally {
      setLoadingUsers(false);
    }
  }, [token, addToast]);

  useEffect(() => {
    if (!isLoading && (!isAuthenticated || user?.role !== 'admin')) {
      router.push('/login');
    } else if (isAuthenticated && user?.role === 'admin' && token) {
      fetchUsers();
    }
  }, [isLoading, isAuthenticated, user, router, token, fetchUsers]);

  const handleDeleteUser = async (userId: string) => {
    if (!confirm('Are you sure you want to delete this user?')) return;

    try {
      await axios.delete(`http://localhost:8000/api/users/${userId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      addToast({
        title: "Success",
        description: "User deleted successfully.",
        type: "success",
      });
      fetchUsers(); // Refresh the list
    } catch (err: unknown) {
      console.error('Failed to delete user:', err);
      const message = axios.isAxiosError(err) && err.response?.data?.detail ? err.response.data.detail : 'Failed to delete user.';
      addToast({
        title: "Error",
        description: message,
        type: "error",
      });
    }
  };

  if (isLoading || (!isAuthenticated && !loadingUsers)) {
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
    return null; // Should have been redirected by useEffect
  }

  const columns: ColumnDef<UserData>[] = [
    {
      accessorKey: 'id',
      header: 'ID',
      enableSorting: true,
    },
    {
      accessorKey: 'username',
      header: 'Username',
      enableSorting: true,
    },
    {
      accessorKey: 'email',
      header: 'Email',
      enableSorting: true,
    },
    {
      accessorKey: 'role',
      header: 'Role',
      enableSorting: true,
    },
    {
      accessorKey: 'tenant_name',
      header: 'Tenant',
      enableSorting: true,
    },
    {
      accessorKey: 'is_active',
      header: 'Active',
      enableSorting: true,
      cell: (row: UserData) => (row.is_active ? 'Yes' : 'No'),
    },
    {
      accessorKey: 'id', // Using ID as accessor for actions
      header: 'Actions',
      enableSorting: false,
      cell: (row: UserData) => (
        <div className="flex space-x-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => router.push(`/admin/users/${row.id}`)}
            title="Edit User"
          >
            <FaPencil />
          </Button>
          <Button
            variant="destructive"
            size="sm"
            onClick={() => handleDeleteUser(row.id)}
            title="Delete User"
          >
            <FaTrashCan />
          </Button>
        </div>
      ),
    },
  ];

  return (
    <div className="space-y-6 p-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Admin User Management</h1>
        <Button onClick={() => router.push('/admin/users/create')}>
          <FaPlus className="mr-2" /> Create New User
        </Button>
      </div>

      {loadingUsers ? (
        <div className="text-center py-8">
          <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <span className="text-gray-600 font-medium">Loading users...</span>
        </div>
      ) : error ? (
        <div className="text-center py-8 text-red-500">{error}</div>
      ) : (
        <div className="overflow-x-auto rounded-lg shadow-md">
          <DataTable columns={columns} data={users} />
        </div>
      )}
    </div>
  );
}

