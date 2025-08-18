// frontend/components/Admin/UserManagement.tsx (Conceptual)

import React, { useState, useEffect } 'react';
import axios from 'axios';
import { useRouter } from 'next/router';

interface UserData {
  id: number;
  username: string;
  email: string;
  role: string;
  tenant_name: string; // Assuming tenant name is available
  is_active: boolean;
  // Add other user fields as needed
}

const UserManagement: React.FC = () => {
  const [users, setUsers] = useState<UserData[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const router = useRouter();

  const getAuthHeaders = () => {
    const token = localStorage.getItem('jwt_token');
    if (!token) {
      router.push('/login');
      return {};
    }
    return { Authorization: `Bearer ${token}` };
  };

  useEffect(() => {
    const fetchUsers = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const headers = getAuthHeaders();
        if (!headers.Authorization) return;

        // Conceptual API endpoint for fetching all users (admin only)
        const response = await axios.get('http://localhost:8000/admin/users', { headers });
        setUsers(response.data);

      } catch (err: any) {
        if (err.response && err.response.data && err.response.data.detail) {
          setError(err.response.data.detail);
        } else {
          setError('Failed to load users. Please ensure you have admin privileges.');
        }
        console.error('User fetch error:', err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchUsers();
  }, []);

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
    // Implement client-side filtering or trigger API call with search term
  };

  const filteredUsers = users.filter(user =>
    user.username.toLowerCase().includes(searchTerm.toLowerCase()) ||
    user.email.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (isLoading) {
    return (
      <div className="elite-container my-10 text-center">
        <div className="loading-spinner mx-auto mb-4"></div>
        <p className="text-soft-text">Loading users...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="elite-container my-10 text-center text-red-500">
        <p>Error: {error}</p>
      </div>
    );
  }

  return (
    <div className="elite-container my-10">
      <h1 className="section-title text-center mb-8">User Management</h1>

      <div className="elite-card p-6 mb-6">
        <div className="flex justify-between items-center mb-4">
          <input
            type="text"
            className="form-input p-2 rounded-lg w-1/3"
            placeholder="Search users..."
            value={searchTerm}
            onChange={handleSearch}
          />
          <button onClick={() => router.push('/admin/users/create')} className="btn-primary px-4 py-2 rounded-lg">
            Create New User
          </button>
        </div>

        {filteredUsers.length === 0 ? (
          <div className="text-center text-soft-text">
            <p>No users found.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full bg-white rounded-lg shadow-md">
              <thead>
                <tr className="bg-gray-100 text-left text-soft-text text-sm font-medium uppercase tracking-wider">
                  <th className="py-3 px-4 rounded-tl-lg">Username</th>
                  <th className="py-3 px-4">Email</th>
                  <th className="py-3 px-4">Role</th>
                  <th className="py-3 px-4">Tenant</th>
                  <th className="py-3 px-4">Status</th>
                  <th className="py-3 px-4 rounded-tr-lg">Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredUsers.map((user) => (
                  <tr key={user.id} className="border-b border-gray-200 hover:bg-gray-50">
                    <td className="py-3 px-4 text-charcoal">{user.username}</td>
                    <td className="py-3 px-4 text-charcoal">{user.email}</td>
                    <td className="py-3 px-4 text-charcoal">{user.role}</td>
                    <td className="py-3 px-4 text-charcoal">{user.tenant_name}</td>
                    <td className="py-3 px-4">
                      <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${user.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                        {user.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </td>
                    <td className="py-3 px-4">
                      <button onClick={() => router.push(`/admin/users/${user.id}/edit`)} className="text-blue-600 hover:text-blue-900 text-sm mr-2">Edit</button>
                      <button onClick={() => alert(`Delete user ${user.username}`)} className="text-red-600 hover:text-red-900 text-sm">Delete</button>
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
};

export default UserManagement;