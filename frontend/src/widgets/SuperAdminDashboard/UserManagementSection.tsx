// frontend/src/widgets/SuperAdminDashboard/UserManagementSection.tsx

import React, { useState, useEffect } from 'react';
import { fetchAllUsers } from './adminService';
import type { UserData } from '@/lib/api'; // Use type from central API
import { Card } from '@/components/ui/card';
import { FaTriangleExclamation, FaSpinner, FaUsers } from 'react-icons/fa6';

const UserManagementSection: React.FC = () => {
  const [users, setUsers] = useState<UserData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const getUsers = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await fetchAllUsers();
        setUsers(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch users.');
      } finally {
        setLoading(false);
      }
    };
    getUsers();
  }, []);

  if (loading) {
    return (
      <Card className="p-4 flex items-center justify-center">
        <FaSpinner className="animate-spin mr-2" /> Loading users...
      </Card>
    );
  }

  if (error) {
    return (
      <Card className="p-4 text-red-600 flex items-center">
        <FaExclamationTriangle className="mr-2" /> Error: {error}
      </Card>
    );
  }

  return (
    <Card className="p-4">
      <h4 className="text-lg font-semibold mb-4 flex items-center"><FaUsers className="mr-2" /> Manage Users</h4>
      <p className="text-gray-600 mb-4">List, create, edit, suspend, and delete users.</p>
      
      <div className="overflow-x-auto">
        <table className="min-w-full bg-white">
          <thead>
            <tr>
              <th className="py-2 px-4 border-b text-left">ID</th>
              <th className="py-2 px-4 border-b text-left">Username</th>
              <th className="py-2 px-4 border-b text-left">Email</th>
              <th className="py-2 px-4 border-b text-left">Role</th>
              <th className="py-2 px-4 border-b text-left">Tenant</th>
              <th className="py-2 px-4 border-b text-left">Active</th>
              <th className="py-2 px-4 border-b text-left">Actions</th>
            </tr>
          </thead>
          <tbody>
            {users.map((user) => (
              <tr key={user.id}>
                <td className="py-2 px-4 border-b text-sm">{user.id}</td>
                <td className="py-2 px-4 border-b text-sm">{user.username}</td>
                <td className="py-2 px-4 border-b text-sm">{user.email}</td>
                <td className="py-2 px-4 border-b text-sm">{user.role}</td>
                <td className="py-2 px-4 border-b text-sm">{user.tenant_name}</td>
                <td className="py-2 px-4 border-b text-sm">{user.is_active ? 'Yes' : 'No'}</td>
                <td className="py-2 px-4 border-b text-sm">
                  <button className="text-blue-600 hover:underline mr-2">Edit</button>
                  <button className="text-red-600 hover:underline">Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  );
};

export default UserManagementSection;
