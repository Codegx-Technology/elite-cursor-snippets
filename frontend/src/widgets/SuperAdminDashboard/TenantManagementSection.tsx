import React, { useState, useEffect } from 'react';
import FormInput from '@/components/FormInput';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { apiClient, Tenant, TenantBrandingData } from '@/lib/api'; // Import Tenant type
import { FaBuilding, FaSpinner, FaExclamationTriangle } from 'react-icons/fa6'; // Added icons

const TenantManagementSection: React.FC = () => {
  const [tenants, setTenants] = useState<Tenant[]>([]);
  const [selectedTenantId, setSelectedTenantId] = useState<string | null>(null);
  const [currentTenant, setCurrentTenant] = useState<TenantBrandingData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [brandingLoading, setBrandingLoading] = useState(false); // Added for branding loading
  const [brandingError, setBrandingError] = useState<string | null>(null); // Added for branding error


  useEffect(() => {
    const fetchTenants = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await apiClient.getSuperAdminTenants();
        if (response.data) {
          setTenants(response.data);
          if (response.data.length > 0) {
            setSelectedTenantId(String(response.data[0].id)); // Ensure ID is string
          }
        } else if (response.error) {
          setError(response.error);
        }
      } catch (err: unknown) {
        setError((err as Error).message || 'Failed to fetch tenants.');
      } finally {
        setLoading(false);
      }
    };

    fetchTenants();
  }, []);

  useEffect(() => {
    if (!selectedTenantId) return;

    const fetchBranding = async () => {
      setBrandingLoading(true); // Use branding specific loading
      setBrandingError(null); // Use branding specific error
      try {
        const response = await apiClient.getTenantBranding(selectedTenantId);
        if (response.data) {
          setCurrentTenant(response.data);
        } else if (response.error) {
          setBrandingError(response.error);
        }
      } catch (err: unknown) {
        setBrandingError((err as Error).message || 'Failed to fetch tenant branding.');
      } finally {
        setBrandingLoading(false); // Use branding specific loading
      }
    };

    fetchBranding();
  }, [selectedTenantId]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setCurrentTenant(prev => prev ? { ...prev, [name]: value } : null);
  };

  const handleSaveBranding = async () => {
    if (!currentTenant || !selectedTenantId) return;

    try {
      // Assuming updateTenantBranding takes tenantId and data
      const response = await apiClient.updateTenantBranding(selectedTenantId, currentTenant);
      if (response.data) {
        alert('Tenant branding saved successfully!');
      } else if (response.error) {
        alert(`Failed to save tenant branding: ${response.error}`);
      }
    } catch (error: unknown) {
      console.error('Failed to save tenant branding:', error);
      alert('Failed to save tenant branding.');
    }
  };

  const getTlsStatusVariant = (status: TenantBrandingData['tls_status']) => {
    switch (status) {
      case 'active':
        return 'success';
      case 'pending':
        return 'warning';
      case 'failed':
        return 'destructive';
      default:
        return 'default';
    }
  };

  if (loading) {
    return (
      <Card className="p-4 flex items-center justify-center">
        <FaSpinner className="animate-spin mr-2" /> Loading tenants...
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
      <h4 className="text-lg font-semibold mb-4 flex items-center"><FaBuilding className="mr-2" /> Manage Tenants</h4>
      <p className="text-gray-600 mb-4">List, create, edit, and manage tenant plans.</p>

      {/* Tenant Listing Table */}
      <div className="mb-6 overflow-x-auto">
        <h5 className="text-md font-medium text-gray-800 mb-2">All Tenants</h5>
        <table className="min-w-full bg-white">
          <thead>
            <tr>
              <th className="py-2 px-4 border-b text-left">ID</th>
              <th className="py-2 px-4 border-b text-left">Name</th>
              <th className="py-2 px-4 border-b text-left">Plan</th>
              <th className="py-2 px-4 border-b text-left">Active</th>
              <th className="py-2 px-4 border-b text-left">Actions</th>
            </tr>
          </thead>
          <tbody>
            {tenants.map(tenant => (
              <tr key={tenant.id}>
                <td className="py-2 px-4 border-b text-sm">{tenant.id}</td>
                <td className="py-2 px-4 border-b text-sm">{tenant.name}</td>
                <td className="py-2 px-4 border-b text-sm">{tenant.plan}</td>
                <td className="py-2 px-4 border-b text-sm">{tenant.is_active ? 'Yes' : 'No'}</td>
                <td className="py-2 px-4 border-b text-sm">
                  <button className="text-blue-600 hover:underline mr-2">Edit</button>
                  <button className="text-red-600 hover:underline">Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Tenant Selection Dropdown */}
      <div className="mb-6">
        <label htmlFor="tenant-select" className="block text-sm font-medium text-gray-700 mb-2">Select Tenant for Branding:</label>
        <select
          id="tenant-select"
          className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm rounded-md"
          value={selectedTenantId === null ? '' : selectedTenantId}
          onChange={(e) => setSelectedTenantId(e.target.value)}
        >
          {tenants.map(tenant => (
            <option key={tenant.id} value={tenant.id}>{tenant.name}</option>
          ))}
        </select>
      </div>

      {brandingLoading ? (
        <div className="bg-gray-50 p-4 rounded-lg text-center">
          <p className="text-gray-600">Loading branding settings...</p>
        </div>
      ) : brandingError ? (
        <div className="bg-red-50 p-4 rounded-lg text-center text-red-600">
          <p>Error: {brandingError}</p>
        </div>
      ) : !currentTenant ? (
        <div className="bg-yellow-50 p-4 rounded-lg text-center text-yellow-700">
          <p>No branding data found for selected tenant.</p>
        </div>
      ) : (
        <div className="space-y-6">
          <h5 className="text-md font-medium text-gray-800">Tenant Branding Settings</h5>
          <FormInput
            label="Tenant Name"
            type="text"
            id="name"
            name="name"
            value={currentTenant.name || ''} // Added default empty string
            onChange={handleInputChange}
          />
          <FormInput
            label="Logo URL"
            type="text"
            id="logo_url"
            name="logo_url"
            value={currentTenant.logo_url || ''} // Added default empty string
            onChange={handleInputChange}
          />
          <FormInput
            label="Primary Color (Hex)"
            type="color"
            id="primary_color"
            name="primary_color"
            value={currentTenant.primary_color || '#000000'} // Added default color
            onChange={handleInputChange}
          />
          <FormInput
            label="Secondary Color (Hex)"
            type="color"
            id="secondary_color"
            name="secondary_color"
            value={currentTenant.secondary_color || '#000000'} // Added default color
            onChange={handleInputChange}
          />
          <FormInput
            label="Custom Domain"
            type="text"
            id="custom_domain"
            name="custom_domain"
            value={currentTenant.custom_domain || ''} // Added default empty string
            onChange={handleInputChange}
          />
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">TLS Status</label>
            <Badge variant={getTlsStatusVariant(currentTenant.tls_status)}>{currentTenant.tls_status}</Badge>
          </div>
          <Button onClick={handleSaveBranding} className="btn-primary">
            Save Branding Settings
          </Button>
        </div>
      )}
    </Card>
  );
};

export default TenantManagementSection;