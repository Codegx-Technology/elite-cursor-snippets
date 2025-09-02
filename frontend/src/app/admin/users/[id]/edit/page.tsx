'use client';

import { useState, useEffect } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { useUserManagement } from '@/hooks/useUserManagement';
import { FaFloppyDisk, FaSpinner } from 'react-icons/fa6';
import Card from '@/components/Card';

export default function EditUserPage() {
  const { user, isLoading, getUser, updateUser } = useUserManagement();
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [role, setRole] = useState('user');
  const [tenantName, setTenantName] = useState('');
  const [isActive, setIsActive] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const router = useRouter();
  const params = useParams();
  const id = Number(params.id);

  useEffect(() => {
    getUser(id);
  }, [id, getUser]);

  useEffect(() => {
    if (user) {
      setUsername(user.username);
      setEmail(user.email);
      setRole(user.role);
      setTenantName(user.tenant_name);
      setIsActive(user.is_active);
    }
  }, [user]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSaving(true);
    await updateUser(id, {
      username,
      email,
      role,
      tenant_name: tenantName,
      is_active: isActive
    });
    setIsSaving(false);
    router.push('/admin/users');
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <FaSpinner className="w-8 h-8 text-green-600 animate-spin mx-auto mb-4" />
          <span className="text-gray-600 font-medium">Loading user...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="elite-container my-10">
      <h1 className="section-title text-center mb-8">Edit User</h1>

      <Card className="p-8 max-w-2xl mx-auto my-10 rounded-xl shadow-lg">
        <form onSubmit={handleSubmit}>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label htmlFor="username" className="block text-sm font-medium text-gray-700">Username</label>
              <input
                type="text"
                id="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="form-input w-full mt-1"
                required
              />
            </div>
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700">Email</label>
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="form-input w-full mt-1"
                required
              />
            </div>
            <div>
              <label htmlFor="role" className="block text-sm font-medium text-gray-700">Role</label>
              <select
                id="role"
                value={role}
                onChange={(e) => setRole(e.target.value)}
                className="form-input w-full mt-1"
              >
                <option value="user">User</option>
                <option value="admin">Admin</option>
              </select>
            </div>
            <div>
              <label htmlFor="tenantName" className="block text-sm font-medium text-gray-700">Tenant Name</label>
              <input
                type="text"
                id="tenantName"
                value={tenantName}
                onChange={(e) => setTenantName(e.target.value)}
                className="form-input w-full mt-1"
              />
            </div>
            <div className="flex items-center">
              <input
                type="checkbox"
                id="isActive"
                checked={isActive}
                onChange={(e) => setIsActive(e.target.checked)}
                className="w-4 h-4 text-green-600 border-gray-300 rounded focus:ring-green-500"
              />
              <label htmlFor="isActive" className="ml-2 text-sm text-gray-700">Active</label>
            </div>
          </div>
          <div className="flex justify-end space-x-4 mt-6">
            <button type="button" onClick={() => router.back()} className="btn-secondary">
              Cancel
            </button>
            <button type="submit" className="btn-primary flex items-center space-x-2" disabled={isSaving}>
              {isSaving ? <FaSpinner className="animate-spin" /> : <FaSave />}
              <span>Save Changes</span>
            </button>
          </div>
        </form>
      </Card>
    </div>
  );
}
