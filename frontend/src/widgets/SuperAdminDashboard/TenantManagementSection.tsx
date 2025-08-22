// frontend/src/widgets/SuperAdminDashboard/TenantManagementSection.tsx

import React, { useState, useEffect } from 'react';
import FormInput from '@/components/FormInput';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { apiClient, TenantBrandingData } from '@/lib/api'; // Import apiClient and TenantBrandingData

const TenantManagementSection: React.FC = () => {
  const [currentTenant, setCurrentTenant] = useState<TenantBrandingData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Dummy tenant ID for now, will be dynamic later
  const tenantId = 'tenant_1'; 

  useEffect(() => {
    const fetchBranding = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await apiClient.getTenantBranding(tenantId);
        if (response.data) {
          setCurrentTenant(response.data);
        } else if (response.error) {
          setError(response.error);
        }
      } catch (err: any) {
        setError(err.message || 'Failed to fetch tenant branding.');
      } finally {
        setLoading(false);
      }
    };

    fetchBranding();
  }, [tenantId]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setCurrentTenant(prev => prev ? { ...prev, [name]: value } : null);
  };

  const handleSaveBranding = async () => {
    // [SNIPPET]: thinkwithai + kenyafirst + surgicalfix
    // [CONTEXT]: Saving tenant branding settings in Super Admin dashboard.
    // [GOAL]: Implement API call to update tenant branding.
    // [TASK]: Call apiClient.updateTenantBranding and handle response.
    if (!currentTenant) return;

    try {
      const response = await apiClient.updateTenantBranding(currentTenant.id, currentTenant);
      if (response.data) {
        alert('Tenant branding saved successfully!');
      } else if (response.error) {
        alert(`Failed to save tenant branding: ${response.error}`);
      }
    } catch (error: any) {
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
      <div className="bg-gray-50 p-4 rounded-lg text-center">
        <p className="text-gray-600">Loading tenant branding settings...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 p-4 rounded-lg text-center text-red-600">
        <p>Error: {error}</p>
      </div>
    );
  }

  if (!currentTenant) {
    return (
      <div className="bg-yellow-50 p-4 rounded-lg text-center text-yellow-700">
        <p>No tenant branding data found.</p>
      </div>
    );
  }

  return (
    <div className="bg-gray-50 p-4 rounded-lg">
      <h4 className="text-lg font-semibold mb-2">Manage Tenants</h4>
      <p className="text-gray-600 mb-4">List, create, edit, and manage tenant plans.</p>

      <div className="space-y-6">
        <h5 className="text-md font-medium text-gray-800">Tenant Branding Settings</h5>
        <FormInput
          label="Tenant Name"
          type="text"
          id="name"
          name="name"
          value={currentTenant.name}
          onChange={handleInputChange}
        />
        <FormInput
          label="Logo URL"
          type="text"
          id="logo_url"
          name="logo_url"
          value={currentTenant.logo_url}
          onChange={handleInputChange}
        />
        <FormInput
          label="Primary Color (Hex)"
          type="color"
          id="primary_color"
          name="primary_color"
          value={currentTenant.primary_color}
          onChange={handleInputChange}
        />
        <FormInput
          label="Secondary Color (Hex)"
          type="color"
          id="secondary_color"
          name="secondary_color"
          value={currentTenant.secondary_color}
          onChange={handleInputChange}
        />
        <FormInput
          label="Custom Domain"
          type="text"
          id="custom_domain"
          name="custom_domain"
          value={currentTenant.custom_domain}
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

      {/* TODO: Implement tenant listing, search, and actions */}
    </div>
  );
};

export default TenantManagementSection;
