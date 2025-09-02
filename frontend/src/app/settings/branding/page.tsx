'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/context/AuthContext';
import { useRouter } from 'next/navigation';
import { apiClient } from '@/lib/api';
import { useToast } from '@/components/ui/use-toast';
import Card from '@/components/Card';
import FormInput from '@/components/FormInput';
import { FaCss3Alt, FaGlobe, FaImage, FaPalette, FaFloppyDisk, FaSpinner } from 'react-icons/fa6';

interface TenantBrandingData {
  logo_url?: string;
  primary_color?: string;
  secondary_color?: string;
  custom_css?: string;
  custom_domain?: string;
  tenant_id?: string;
  tls_status?: string;
  name?: string;
}

export default function BrandingSettingsPage() {
  const { user, isAuthenticated, isLoading: authLoading } = useAuth();
  const router = useRouter();
  const { addToast } = useToast();

  const [brandingData, setBrandingData] = useState<TenantBrandingData>({});
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    if (!authLoading && (!isAuthenticated || user?.role !== 'admin')) {
      router.push('/login');
    } else if (isAuthenticated && user?.role === 'admin') {
      fetchBrandingData();
    }
  }, [authLoading, isAuthenticated, user, router]);

  const fetchBrandingData = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await apiClient.getTenantBranding();
      if (response.data) {
        setBrandingData(response.data);
      } else if (response.error) {
        setError(response.error);
      }
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Failed to fetch branding data.';
      setError(message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { id, value } = e.target;
    setBrandingData(prev => ({ ...prev, [id]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSaving(true);
    setError(null);
    try {
      const response = await apiClient.updateTenantBranding(brandingData);
      if (response.data) {
        addToast({
          title: 'Success',
          description: 'Branding settings updated successfully.',
          type: 'success',
        });
      } else if (response.error) {
        setError(response.error);
      }
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Failed to update branding settings.';
      setError(message);
    } finally {
      setIsSaving(false);
    }
  };

  const handleApplyTLS = async () => {
    setIsSaving(true);
    setError(null);
    try {
      const response = await apiClient.applyTenantTLS(brandingData.custom_domain || '');
      if (response.data) {
        addToast({
          title: 'Success',
          description: 'TLS certificate application initiated. Status will update shortly.',
          type: 'success',
        });
        fetchBrandingData(); // Refresh status
      } else if (response.error) {
        setError(response.error);
      }
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Failed to apply TLS certificate.';
      setError(message);
    } finally {
      setIsSaving(false);
    }
  };

  const handleRemoveCustomDomain = async () => {
    setIsSaving(true);
    setError(null);
    try {
      const response = await apiClient.removeTenantCustomDomain();
      if (response.data) {
        addToast({
          title: 'Success',
          description: 'Custom domain removed successfully.',
          type: 'success',
        });
        fetchBrandingData(); // Refresh status
      } else if (response.error) {
        setError(response.error);
      }
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Failed to remove custom domain.';
      setError(message);
    } finally {
      setIsSaving(false);
    }
  };

  if (authLoading || isLoading) {
    return (
      <div className="flex justify-center items-center min-h-screen-content">
        <FaSpinner className="animate-spin text-4xl text-green-600" />
        <p className="ml-4 text-gray-600">Loading branding settings...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex justify-center items-center min-h-screen-content">
        <p className="text-red-600">Error: {error}</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-4 sm:p-6 lg:p-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-6 flex items-center">
        <FaPalette className="mr-3 text-purple-600" /> Branding Settings
      </h1>

      <form onSubmit={handleSubmit} className="space-y-6">
        <Card className="p-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
            <FaImage className="mr-2 text-blue-600" /> Logo & Colors
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <FormInput
              id="logo_url"
              label="Logo URL"
              type="text"
              value={brandingData.logo_url || ''}
              onChange={handleInputChange}
              placeholder="https://yourdomain.com/logo.png"
              helperText="URL to your brand logo (e.g., for email templates, custom dashboards)."
            />
            <FormInput
              id="primary_color"
              label="Primary Color"
              type="color"
              value={brandingData.primary_color || '#00A651'}
              onChange={handleInputChange}
              helperText="Main brand color (e.g., for buttons, highlights)."
            />
            <FormInput
              id="secondary_color"
              label="Secondary Color"
              type="color"
              value={brandingData.secondary_color || '#FF6B35'}
              onChange={handleInputChange}
              helperText="Secondary brand color (e.g., for accents, secondary elements)."
            />
          </div>
        </Card>

        <Card className="p-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
            <FaCss3Alt className="mr-2 text-orange-600" /> Custom CSS
          </h2>
          <FormInput
            id="custom_css"
            label="Custom CSS"
            type="textarea"
            value={brandingData.custom_css || ''}
            onChange={handleInputChange}
            placeholder="body { font-family: 'Inter', sans-serif; }"
            helperText="Apply custom CSS rules to your branded pages. Use with caution."
            rows={8}
          />
        </Card>

        <Card className="p-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
            <FaGlobe className="mr-2 text-green-600" /> Custom Domain
          </h2>
          <FormInput
            id="custom_domain"
            label="Custom Domain"
            type="text"
            value={brandingData.custom_domain || ''}
            onChange={handleInputChange}
            placeholder="app.yourdomain.com"
            helperText="Point your custom domain to Shujaa Studio. Requires DNS configuration."
          />
          <div className="mt-4 flex items-center space-x-4">
            <button
              type="button"
              onClick={handleApplyTLS}
              disabled={isSaving || !brandingData.custom_domain}
              className="btn-primary flex items-center space-x-2"
            >
              {isSaving ? <FaSpinner className="animate-spin" /> : <FaFloppyDisk />}
              <span>Apply TLS Certificate</span>
            </button>
            {brandingData.tls_status && (
              <span className={`text-sm font-medium ${brandingData.tls_status === 'active' ? 'text-green-600' : 'text-red-600'}`}>
                TLS Status: {brandingData.tls_status}
              </span>
            )}
            {brandingData.custom_domain && (
              <button
                type="button"
                onClick={handleRemoveCustomDomain}
                disabled={isSaving}
                className="btn-secondary flex items-center space-x-2"
              >
                {isSaving ? <FaSpinner className="animate-spin" /> : null}
                <span>Remove Custom Domain</span>
              </button>
            )}
          </div>
        </Card>

        <div className="flex justify-end">
          <button
            type="submit"
            disabled={isSaving}
            className="btn-primary flex items-center space-x-2"
          >
            {isSaving ? <FaSpinner className="animate-spin" /> : <FaFloppyDisk />}
            <span>{isSaving ? 'Saving...' : 'Save Branding Settings'}</span>
          </button>
        </div>
      </form>
    </div>
  );
}

