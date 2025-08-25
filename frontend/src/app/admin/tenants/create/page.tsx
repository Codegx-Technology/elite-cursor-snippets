'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useTenantManagement } from '@/hooks/useTenantManagement';
import { FaPlus, FaSpinner } from 'react-icons/fa';
import Card from '@/components/Card';

export default function CreateTenantPage() {
  const { createTenant } = useTenantManagement();
  const [name, setName] = useState('');
  const [isActive, setIsActive] = useState(true);
  const [plan, setPlan] = useState('free'); // Default plan
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    await createTenant({
      name,
      is_active: isActive,
      plan,
    });
    setIsLoading(false);
    router.push('/admin/tenants');
  };

  return (
    <div className="elite-container my-10">
      <h1 className="section-title text-center mb-8">Create New Tenant</h1>

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
            <button type="submit" className="btn-primary flex items-center space-x-2" disabled={isLoading}>
              {isLoading ? <FaSpinner className="animate-spin" /> : <FaPlus />}
              <span>Create Tenant</span>
            </button>
          </div>
        </form>
      </Card>
    </div>
  );
}

