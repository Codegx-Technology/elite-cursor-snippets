'use client';

import { useState, useEffect } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { useTenantManagement } from '@/hooks/useTenantManagement';
import { FaFloppyDisk, FaSpinner } from 'react-icons/fa6';
import Card from '@/components/Card';

export default function EditTenantPage() {
  const { tenant, isLoading, getTenant, updateTenant } = useTenantManagement();
  const [name, setName] = useState('');
  const [isActive, setIsActive] = useState(true);
  const [plan, setPlan] = useState('free');
  const [isSaving, setIsSaving] = useState(false);
  const router = useRouter();
  const params = useParams();
  const id = Number(params.id);

  useEffect(() => {
    getTenant(id);
  }, [id, getTenant]);

  useEffect(() => {
    if (tenant) {
      setName(tenant.name);
      setIsActive(tenant.is_active);
      setPlan(tenant.plan);
    }
  }, [tenant]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSaving(true);
    await updateTenant(id, {
      name,
      is_active: isActive,
      plan,
    });
    setIsSaving(false);
    router.push('/admin/tenants');
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <FaSpinner className="w-8 h-8 text-green-600 animate-spin mx-auto mb-4" />
          <span className="text-gray-600 font-medium">Loading tenant...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="elite-container my-10">
      <h1 className="section-title text-center mb-8">Edit Tenant</h1>

      <Card className="p-8 max-w-2xl mx-auto my-10 rounded-xl shadow-lg">
        <form onSubmit={handleSubmit}>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-gray-700">Tenant Name</label>
              <input
                type="text"
                id="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="form-input w-full mt-1"
                required
              />
            </div>
            <div>
              <label htmlFor="plan" className="block text-sm font-medium text-gray-700">Plan</label>
              <select
                id="plan"
                value={plan}
                onChange={(e) => setPlan(e.target.value)}
                className="form-input w-full mt-1"
              >
                <option value="free">Free</option>
                <option value="starter">Starter</option>
                <option value="professional">Professional</option>
                <option value="enterprise">Enterprise</option>
              </select>
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
              {isSaving ? <FaSpinner className="animate-spin" /> : <FaFloppyDisk />}
              <span>Save Changes</span>
            </button>
          </div>
        </form>
      </Card>
    </div>
  );
}
