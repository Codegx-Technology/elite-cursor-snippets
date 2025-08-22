'use client';

import React, { useState, useEffect } from 'react';
import FormInput from '@/components/FormInput';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { apiClient, TenantBrandingData } from '@/lib/api';
import { useAuth } from '@/context/AuthContext';

const BrandingSettingsPage: React.FC = () => {
  const { user } = useAuth();
  const [branding, setBranding] = useState<TenantBrandingData | null>(null);
  const [customDomain, setCustomDomain] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!user?.tenant_id) return;

    const fetchBranding = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await apiClient.getTenantBranding(user.tenant_id);
        if (response.data) {
          setBranding(response.data);
          setCustomDomain(response.data.custom_domain || "");
        } else if (response.error) {
          setError(response.error);
        }
      } catch (err: any) {
        setError(err.message || 'Failed to fetch branding settings.');
      } finally {
        setLoading(false);
      }
    };

    fetchBranding();
  }, [user]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setBranding(prev => prev ? { ...prev, [name]: value } : null);
  };

  const handleCustomDomainChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setCustomDomain(e.target.value);
  };

  const handleSaveBranding = async () => {
    if (!branding) return;

    try {
      const response = await apiClient.updateTenantBranding(branding.tenant_id, branding);
      if (response.data) {
        alert('Branding settings saved successfully!');
      } else if (response.error) {
        alert(`Failed to save branding settings: ${response.error}`);
      }
    } catch (error: any) {
      console.error('Failed to save branding settings:', error);
      alert('Failed to save branding settings.');
    }
  };

  const handleSetCustomDomain = async () => {
    if (!customDomain) return;

    try {
      const response = await apiClient.setCustomDomain({ domain: customDomain });
      if (response.data) {
        alert('Custom domain updated successfully! TLS provisioning is in progress.');
      } else if (response.error) {
        alert(`Failed to set custom domain: ${response.error}`);
      }
    } catch (error: any) {
      console.error('Failed to set custom domain:', error);
      alert('Failed to set custom domain.');
    }
  };

  const handleDeleteCustomDomain = async () => {
    if (!confirm('Are you sure you want to delete your custom domain?')) return;

    try {
      const response = await apiClient.deleteCustomDomain();
      if (response.data) {
        alert('Custom domain deleted successfully!');
        setCustomDomain("");
      } else if (response.error) {
        alert(`Failed to delete custom domain: ${response.error}`);
      }
    } catch (error: any) {
      console.error('Failed to delete custom domain:', error);
      alert('Failed to delete custom domain.');
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
    return <p>Loading branding settings...</p>;
  }

  if (error) {
    return <p>Error: {error}</p>;
  }

  if (!branding) {
    return <p>No branding settings found.</p>;
  }

  return (
    <div className="space-y-6">
      <h3 className="text-xl font-semibold">Branding Settings</h3>
      <FormInput
        label="Company Name"
        type="text"
        id="name"
        name="name"
        value={branding.name}
        onChange={handleInputChange}
      />
      <FormInput
        label="Logo URL"
        type="text"
        id="logo_url"
        name="logo_url"
        value={branding.logo_url}
        onChange={handleInputChange}
      />
      <FormInput
        label="Primary Color"
        type="color"
        id="primary_color"
        name="primary_color"
        value={branding.primary_color}
        onChange={handleInputChange}
      />
      <FormInput
        label="Secondary Color"
        type="color"
        id="secondary_color"
        name="secondary_color"
        value={branding.secondary_color}
        onChange={handleInputChange}
      />
      <h3 className="text-xl font-semibold">Custom Domain</h3>
      <div className="space-y-4">
        <FormInput
          label="Custom Domain"
          type="text"
          id="custom_domain"
          name="custom_domain"
          value={customDomain}
          onChange={handleCustomDomainChange}
          placeholder="e.g., my.domain.com"
        />
        <div className="flex items-center space-x-4">
          <Button onClick={handleSetCustomDomain}>Set Custom Domain</Button>
          {branding.custom_domain && (
            <Button variant="destructive" onClick={handleDeleteCustomDomain}>Delete Custom Domain</Button>
          )}
        </div>
        <div>
          <label>TLS Status</label>
          <Badge variant={getTlsStatusVariant(branding.tls_status)}>{branding.tls_status}</Badge>
        </div>
      </div>
      <Button onClick={handleSaveBranding}>Save Branding</Button>
    </div>
  );
};

export default BrandingSettingsPage;
