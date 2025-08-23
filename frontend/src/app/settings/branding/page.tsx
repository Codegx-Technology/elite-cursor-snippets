'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/context/AuthContext';
import { useRouter } from 'next/navigation';
import { apiClient } from '@/lib/api';
import { useToast } from '@/components/ui/use-toast';
import Card from '@/components/Card';
import FormInput from '@/components/FormInput';
import { FaSave, FaSpinner, FaPalette, FaGlobe, FaCss3Alt, FaImage, FaTrash } from 'react-icons/fa';

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
