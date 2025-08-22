"use client";

import React, { useEffect, useState } from 'react';
import { useAuth } from '@/context/AuthContext';
import { useRouter } from 'next/navigation';
import axios from 'axios';
import {
  Table,
  TableHeader,
  TableRow,
  TableHead,
  TableBody,
TableCell,
} from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { useToast } from '@/components/ui/use-toast';
import { FaEdit, FaTrash, FaPlus } from 'react-icons/fa';

interface UserData {
  id: string;
  username: string;
  email: string;
  role: string;
  tenant_name: string;
  is_active: boolean;
}

export default function AdminUsersPage() {
  const { user, isAuthenticated, isLoading, token } = useAuth();
  const router = useRouter();
  const [users, setUsers] = useState<UserData[]>([]);
  const [loadingUsers, setLoadingUsers] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { addToast } = useToast();

  const fetchUsers = async () => {
    setLoadingUsers(true);
    setError(null);
    try {
      const response = await axios.get('http://localhost:8000/api/users', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setUsers(response.data);
    } catch (err: any) {
      console.error('Failed to fetch users:', err);
      setError(err.response?.data?.detail || 'Failed to fetch users.');
      addToast({
        title: "Error",
        description: err.response?.data?.detail || 'Failed to fetch users.',
        type: "error",
      });
    } finally {
      setLoadingUsers(false);
    }
  };

  useEffect(() => {
    if (!isLoading && (!isAuthenticated || user?.role !== 'admin')) {
      router.push('/login');
    } else if (isAuthenticated && user?.role === 'admin' && token) {
      fetchUsers();
    }
  }, [isLoading, isAuthenticated, user, router, token]);

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
    } catch (err: any) {
      console.error('Failed to delete user:', err);
      addToast({
        title: "Error",
        description: err.response?.data?.detail || 'Failed to delete user.',
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
          <Table className="min-w-full bg-white">
            <TableHeader>
              <TableRow>
                <TableHead className="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</TableHead>
                <TableHead className="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Username</TableHead>
                <TableHead className="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</TableHead>
                <TableHead className="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Role</TableHead>
                <TableHead className="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Tenant</TableHead>
                <TableHead className="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Active</TableHead>
                <TableHead className="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {users.map((u) => (
                <TableRow key={u.id} className="border-b border-gray-200 hover:bg-gray-50">
                  <TableCell className="py-4 px-4 whitespace-nowrap text-sm font-medium text-gray-900">{u.id}</TableCell>
                  <TableCell className="py-4 px-4 whitespace-nowrap text-sm text-gray-700">{u.username}</TableCell>
                  <TableCell className="py-4 px-4 whitespace-nowrap text-sm text-gray-700">{u.email}</TableCell>
                  <TableCell className="py-4 px-4 whitespace-nowrap text-sm text-gray-700">{u.role}</TableCell>
                  <TableCell className="py-4 px-4 whitespace-nowrap text-sm text-gray-700">{u.tenant_name}</TableCell>
                  <TableCell className="py-4 px-4 whitespace-nowrap text-sm text-gray-700">{u.is_active ? 'Yes' : 'No'}</TableCell>
                  <TableCell className="py-4 px-4 whitespace-nowrap text-sm font-medium">
                    <div className="flex space-x-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => router.push(`/admin/users/${u.id}`)}
                        title="Edit User"
                      >
                        <FaEdit />
                      </Button>
                      <Button
                        variant="destructive"
                        size="sm"
                        onClick={() => handleDeleteUser(u.id)}
                        title="Delete User"
                      >
                        <FaTrash />
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      )}
    </div>
  );
}
