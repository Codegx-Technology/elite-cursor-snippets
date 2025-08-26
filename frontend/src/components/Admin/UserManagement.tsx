'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useUserManagement, UserData } from '@/hooks/useUserManagement';
import { FaSpinner, FaTrash, FaEdit, FaPlus } from 'react-icons/fa';
import Card from '@/components/Card';
import DeleteUserModal from '@/components/Admin/DeleteUserModal';

// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorclean
// [CONTEXT]: Reusable user management component
// [GOAL]: Provide a clean and reusable component for managing users

export default function UserManagement() {
  const { users, isLoading, error, deleteUser } = useUserManagement();
  const [searchTerm, setSearchTerm] = useState('');
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [selectedUser, setSelectedUser] = useState<UserData | null>(null);
  const router = useRouter();

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
  };

  const openDeleteModal = (user: UserData) => {
    setSelectedUser(user);
    setShowDeleteModal(true);
  };

  const handleDeleteUser = async (id: number) => {
    await deleteUser(id);
    setShowDeleteModal(false);
  };

  const filteredUsers = users.filter(user =>
    user.username.toLowerCase().includes(searchTerm.toLowerCase()) ||
    user.email.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <FaSpinner className="w-8 h-8 text-green-600 animate-spin mx-auto mb-4" />
          <span className="text-gray-600 font-medium">Loading users...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-red-500 text-center">
        <p>Error: {error}</p>
      </div>
    );
  }

  return (
    <div className="elite-container my-10">
      <DeleteUserModal isOpen={showDeleteModal} onClose={() => setShowDeleteModal(false)} onDelete={handleDeleteUser} user={selectedUser} />

      <h1 className="section-title text-center mb-8">User Management</h1>

      <Card className="p-6 mb-6">
        <div className="flex justify-between items-center mb-4">
          <input
            type="text"
            className="form-input p-2 rounded-lg w-1/3"
            placeholder="Search users..."
            value={searchTerm}
            onChange={handleSearch}
          />
          <button onClick={() => router.push('/admin/users/create')} className="btn-primary px-4 py-2 rounded-lg flex items-center space-x-2">
            <FaPlus />
            <span>Create New User</span>
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
                      <button onClick={() => router.push(`/admin/users/${user.id}/edit`)} className="text-blue-600 hover:text-blue-900 text-sm mr-2">
                        <FaEdit />
                      </button>
                      <button onClick={() => openDeleteModal(user)} className="text-red-600 hover:text-red-900 text-sm">
                        <FaTrash />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>
    </div>
  );
}

