'use client';

import React, { useState, useEffect } from 'react';
import FormInput from '@/components/FormInput';
import Card from '@/components/Card';
import LoadingStates from '@/components/ui/LoadingStates';
import ErrorStates from '@/components/ui/ErrorStates';
import { apiClient, ApiKey, Integration, NotificationPreferences, SecuritySettings, LoginSession, StorageInfo, LocalModel } from '@/lib/api';
import { Table, TableHeader, TableRow, TableHead, TableBody, TableCell } from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { useToast } from '@/components/ui/use-toast';
import BrandingSettingsPage from './branding/page';

export default function SettingsPage() {
  const [activeTab, setActiveTab] = useState('profile');

  const [apiKeys, setApiKeys] = useState<ApiKey[]>([]);
  const [apiKeysLoading, setApiKeysLoading] = useState(true);
  const [apiKeysError, setApiKeysError] = useState<string | null>(null);

  const [integrations, setIntegrations] = useState<Integration[]>([]);
  const [integrationsLoading, setIntegrationsLoading] = useState(true);
  const [integrationsError, setIntegrationsError] = useState<string | null>(null);

  const [preferences, setPreferences] = useState<NotificationPreferences | null>(null);
  const [preferencesLoading, setPreferencesLoading] = useState(true);
  const [preferencesError, setPreferencesError] = useState<string | null>(null);

  const [securitySettings, setSecuritySettings] = useState<SecuritySettings | null>(null);
  const [securitySettingsLoading, setSecuritySettingsLoading] = useState(true);
  const [securitySettingsError, setSecuritySettingsError] = useState<string | null>(null);

  const [loginSessions, setLoginSessions] = useState<LoginSession[]>([]);
  const [sessionsLoading, setSessionsLoading] = useState(true);
  const [sessionsError, setSessionsError] = useState<string | null>(null);

  const [storageInfo, setStorageInfo] = useState<StorageInfo | null>(null);
  const [storageLoading, setStorageLoading] = useState(true);
  const [storageError, setStorageError] = useState<string | null>(null);

  const [localModels, setLocalModels] = useState<LocalModel[]>([]);
  const [localModelsLoading, setLocalModelsLoading] = useState(true);
  const [localModelsError, setLocalModelsError] = useState<string | null>(null);

  const { addToast } = useToast();

  useEffect(() => {
    const fetchApiKeys = async () => {
      setApiKeysLoading(true);
      setApiKeysError(null);
      try {
        const response = await apiClient.getApiKeys();
        if (response.data) {
          setApiKeys(response.data);
        } else if (response.error) {
          setApiKeysError(response.error);
        }
      } catch (err: any) {
        setApiKeysError(err.message || 'Failed to fetch API keys.');
      } finally {
        setApiKeysLoading(false);
      }
    };

    const fetchIntegrations = async () => {
      setIntegrationsLoading(true);
      setIntegrationsError(null);
      try {
        const response = await apiClient.getIntegrations();
        if (response.data) {
          setIntegrations(response.data);
        } else if (response.error) {
          setIntegrationsError(response.error);
        }
      } catch (err: any) {
        setIntegrationsError(err.message || 'Failed to fetch integrations.');
      } finally {
        setIntegrationsLoading(false);
      }
    };

    const fetchPreferences = async () => {
      setPreferencesLoading(true);
      setPreferencesError(null);
      try {
        const response = await apiClient.getNotificationPreferences();
        if (response.data) {
          setPreferences(response.data);
        } else if (response.error) {
          setPreferencesError(response.error);
        }
      } catch (err: any) {
        setPreferencesError(err.message || 'Failed to fetch notification preferences.');
      } finally {
        setPreferencesLoading(false);
      }
    };

    const fetchSecuritySettings = async () => {
      setSecuritySettingsLoading(true);
      setSecuritySettingsError(null);
      try {
        const response = await apiClient.getSecuritySettings();
        if (response.data) {
          setSecuritySettings(response.data);
        } else if (response.error) {
          setSecuritySettingsError(response.error);
        }
      } catch (err: any) {
        setSecuritySettingsError(err.message || 'Failed to fetch security settings.');
      } finally {
        setSecuritySettingsLoading(false);
      }
    };

    const fetchLoginSessions = async () => {
      setSessionsLoading(true);
      setSessionsError(null);
      try {
        const response = await apiClient.getLoginSessions();
        if (response.data) {
          setLoginSessions(response.data);
        } else if (response.error) {
          setSessionsError(response.error);
        }
      } catch (err: any) {
        setSessionsError(err.message || 'Failed to fetch login sessions.');
      } finally {
        setSessionsLoading(false);
      }
    };

    const fetchStorageInfo = async () => {
      setStorageLoading(true);
      setStorageError(null);
      try {
        const response = await apiClient.getStorageInfo();
        if (response.data) {
          setStorageInfo(response.data);
        } else if (response.error) {
          setStorageError(response.error);
        }
      } catch (err: any) {
        setStorageError(err.message || 'Failed to fetch storage information.');
      } finally {
        setStorageLoading(false);
      }
    };

    const fetchLocalModels = async () => {
      setLocalModelsLoading(true);
      setLocalModelsError(null);
      try {
        const response = await apiClient.getLocalModels();
        if (response.data) {
          setLocalModels(response.data);
        } else if (response.error) {
          setLocalModelsError(response.error);
        }
      } catch (err: any) {
        setLocalModelsError(err.message || 'Failed to fetch local models.');
      } finally {
        setLocalModelsLoading(false);
      }
    };

    fetchApiKeys();
    fetchIntegrations();
    fetchPreferences();
    fetchSecuritySettings();
    fetchLoginSessions();
    fetchStorageInfo();
    fetchLocalModels();
  }, []);

  const handleGenerateApiKey = async () => {
    try {
      const response = await apiClient.generateApiKey();
      if (response.data) {
        setApiKeys(prev => response.data ? [...prev, response.data] : prev);
        addToast({ title: "API Key Generated", description: "A new API key has been generated.", type: "success" });
      } else if (response.error) {
        addToast({ title: "API Key Generation Failed", description: response.error, type: "destructive" });
      }
    } catch (err: any) {
      addToast({ title: "API Key Generation Failed", description: err.message || "An unexpected error occurred.", type: "destructive" });
    }
  };

  const handleRevokeApiKey = async (id: string) => {
    if (!confirm('Are you sure you want to revoke this API key?')) return;
    try {
      const response = await apiClient.revokeApiKey(id);
      if (response.data?.success) {
        setApiKeys(prev => prev.filter(key => key.id !== id));
        addToast({ title: "API Key Revoked", description: "The API key has been revoked.", type: "success" });
      } else if (response.error) {
        addToast({ title: "API Key Revocation Failed", description: response.error, type: "destructive" });
      }
    } catch (err: any) {
      addToast({ title: "API Key Revocation Failed", description: err.message || "An unexpected error occurred.", type: "destructive" });
    }
  };

  const handleUpdateIntegration = async (id: string, config: Record<string, unknown>) => {
    try {
      const response = await apiClient.updateIntegration(id, config);
      if (response.data) {
        setIntegrations(prev => response.data ? prev.map(integration => integration.id === id ? response.data as Integration : integration) : prev);
        addToast({ title: "Integration Updated", description: `Integration ${response.data.name} updated successfully.`, type: "success" });
      } else if (response.error) {
        addToast({ title: "Integration Update Failed", description: response.error, type: "destructive" });
      }
    } catch (err: any) {
      addToast({ title: "Integration Update Failed", description: err.message || "An unexpected error occurred.", type: "destructive" });
    }
  };

  const handlePreferenceChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, checked } = e.target;
    setPreferences(prev => prev ? { ...prev, [name]: checked } : null);
  };

  const handleSavePreferences = async () => {
    // [SNIPPET]: thinkwithai + kenyafirst + surgicalfix
    // [CONTEXT]: Saving notification preferences in Settings page.
    // [GOAL]: Implement API call to update notification preferences.
    // [TASK]: Call apiClient.updateNotificationPreferences and handle response.
    if (!preferences) return;

    try {
      const response = await apiClient.updateNotificationPreferences(preferences);
      if (response.data) {
        addToast({ title: "Preferences Saved", description: "Notification preferences updated successfully.", type: "success" });
      } else if (response.error) {
        addToast({ title: "Save Failed", description: response.error, type: "destructive" });
      }
    } catch (err: any) {
      addToast({ title: "Save Failed", description: err.message || "An unexpected error occurred.", type: "destructive" });
    }
  };

  const handleToggle2FA = async () => {
    if (!securitySettings) return;
    try {
      const response = securitySettings.two_factor_enabled
        ? await apiClient.disableTwoFactorAuth()
        : await apiClient.enableTwoFactorAuth();

      if (response.data?.success) {
        setSecuritySettings(prev => prev ? { ...prev, two_factor_enabled: !prev.two_factor_enabled } : null);
        addToast({ title: "2FA Updated", description: `Two-factor authentication ${securitySettings.two_factor_enabled ? 'disabled' : 'enabled'} successfully.`, type: "success" });
        // If 2FA was just enabled, and QR code is returned, display it (e.g., in a modal)
        if (!securitySettings.two_factor_enabled && response.data) {
          const data = response.data as { success: boolean; qr_code_url?: string; secret?: string };
          if (data.qr_code_url) {
            alert(`Scan this QR code to enable 2FA: ${data.qr_code_url}`);
          }
        }
      } else if (response.error) {
        addToast({ title: "2FA Update Failed", description: response.error, type: "destructive" });
      }
    } catch (err: any) {
      addToast({ title: "2FA Update Failed", description: err.message || "An unexpected error occurred.", type: "destructive" });
    }
  };

  const handleRevokeSession = async (sessionId: string) => {
    if (!confirm('Are you sure you want to revoke this login session?')) return;
    try {
      const response = await apiClient.revokeLoginSession(sessionId);
      if (response.data?.success) {
        setLoginSessions(prev => prev.filter(session => session.id !== sessionId));
        addToast({ title: "Session Revoked", description: "Login session revoked successfully.", type: "success" });
      } else if (response.error) {
        addToast({ title: "Session Revocation Failed", description: response.error, type: "destructive" });
      }
    } catch (err: any) {
      addToast({ title: "Session Revocation Failed", description: err.message || "An unexpected error occurred.", type: "destructive" });
    }
  };

  const handleClearCache = async () => {
    if (!confirm('Are you sure you want to clear the cache? This cannot be undone.')) return;
    try {
      const response = await apiClient.clearCache();
      if (response.data?.success) {
        addToast({ title: "Cache Cleared", description: "Application cache cleared successfully.", type: "success" });
        // Optionally refetch storage info
        // fetchStorageInfo();
      } else if (response.error) {
        addToast({ title: "Cache Clear Failed", description: response.error, type: "destructive" });
      }
    } catch (err: any) {
      addToast({ title: "Cache Clear Failed", description: err.message || "An unexpected error occurred.", type: "destructive" });
    }
  };

  const handleDownloadModel = async (modelId: string) => {
    try {
      const response = await apiClient.downloadLocalModel(modelId);
      if (response.data?.success) {
        addToast({ title: "Model Download Started", description: "Model download initiated.", type: "info" });
        // Optionally update local model status to downloading
        setLocalModels(prev => prev.map(model => model.id === modelId ? { ...model, status: 'downloading', download_progress: 0 } : model));
      } else if (response.error) {
        addToast({ title: "Model Download Failed", description: response.error, type: "destructive" });
      }
    } catch (err: any) {
      addToast({ title: "Model Download Failed", description: err.message || "An unexpected error occurred.", type: "destructive" });
    }
  };

  const handleDeleteModel = async (modelId: string) => {
    if (!confirm('Are you sure you want to delete this local model?')) return;
    try {
      const response = await apiClient.deleteLocalModel(modelId);
      if (response.data?.success) {
        setLocalModels(prev => prev.filter(model => model.id !== modelId));
        addToast({ title: "Model Deleted", description: "Local model deleted successfully.", type: "success" });
      } else if (response.error) {
        addToast({ title: "Model Deletion Failed", description: response.error, type: "destructive" });
      }
    } catch (err: any) {
      addToast({ title: "Model Deletion Failed", description: err.message || "An unexpected error occurred.", type: "destructive" });
    }
  };

  const renderContent = () => {
    switch (activeTab) {
      case 'profile':
        return (
          <form>
            <FormInput
              label="Username"
              type="text"
              placeholder="Enter your username"
              id="username"
              name="username"
            />
            <FormInput
              label="Email"
              type="email"
              placeholder="Enter your email"
              id="email"
              name="email"
            />
            <FormInput
              label="New Password"
              type="password"
              placeholder="Enter new password"
              id="newPassword"
              name="newPassword"
            />
            <FormInput
              label="Confirm New Password"
              type="password"
              placeholder="Confirm new password"
              id="confirmNewPassword"
              name="confirmNewPassword"
            />
            <button type="submit" className="btn-primary mt-4">Save Profile</button>
          </form>
        );
      case 'api-integrations':
        return (
          <div>
            <h3 className="text-xl font-semibold mb-4">API Keys</h3>
            {apiKeysLoading ? (
              <p className="text-gray-600">Loading API keys...</p>
            ) : apiKeysError ? (
              <p className="text-red-600">Error loading API keys: {apiKeysError}</p>
            ) : apiKeys.length === 0 ? (
              <div className="text-center">
                <p className="text-gray-500">No API keys found.</p>
                <Button onClick={handleGenerateApiKey} className="mt-4">Generate New API Key</Button>
              </div>
            ) : (
              <div className="overflow-x-auto mb-8">
                <Table className="min-w-full bg-white shadow-md rounded-lg overflow-hidden">
                  <TableHeader>
                    <TableRow>
                      <TableHead>Key</TableHead>
                      <TableHead>Created At</TableHead>
                      <TableHead>Last Used</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead>Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {apiKeys.map((key) => (
                      <TableRow key={key.id}>
                        <TableCell className="font-mono text-sm">{key.key}</TableCell>
                        <TableCell>{new Date(key.created_at).toLocaleDateString()}</TableCell>
                        <TableCell>{key.last_used_at ? new Date(key.last_used_at).toLocaleDateString() : 'Never'}</TableCell>
                        <TableCell>
                          <Badge variant={key.is_active ? 'success' : 'destructive'}>
                            {key.is_active ? 'Active' : 'Inactive'}
                          </Badge>
                        </TableCell>
                        <TableCell>
                          <Button variant="destructive" size="sm" onClick={() => handleRevokeApiKey(key.id)}>
                            Revoke
                          </Button>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
                <div className="text-right mt-4">
                  <Button onClick={handleGenerateApiKey}>Generate New API Key</Button>
                </div>
              </div>
            )}

            <h3 className="text-xl font-semibold mb-4">Integrations</h3>
            {integrationsLoading ? (
              <p className="text-gray-600">Loading integrations...</p>
            ) : integrationsError ? (
              <p className="text-red-600">Error loading integrations: {integrationsError}</p>
            ) : integrations.length === 0 ? (
              <p className="text-gray-500">No integrations available.</p>
            ) : (
              <div className="space-y-4">
                {integrations.map((integration) => (
                  <div key={integration.id} className="bg-white p-4 rounded-lg shadow-sm flex items-center justify-between">
                    <div>
                      <h4 className="font-medium text-gray-800">{integration.name} ({integration.type})</h4>
                      <p className="text-sm text-gray-600">Status: <Badge variant={integration.is_enabled ? 'success' : 'destructive'}>{integration.is_enabled ? 'Enabled' : 'Disabled'}</Badge></p>
                    </div>
                    <Button size="sm" onClick={() => handleUpdateIntegration(integration.id, { is_enabled: !integration.is_enabled })}>
                      {integration.is_enabled ? 'Disable' : 'Enable'}
                    </Button>
                  </div>
                ))}
              </div>
            )}
          </div>
        );
      case 'notifications':
        return (
          <div>
            <h3 className="text-xl font-semibold mb-4">Notification Preferences</h3>
            {preferencesLoading ? (
              <p className="text-gray-600">Loading preferences...</p>
            ) : preferencesError ? (
              <p className="text-red-600">Error loading preferences: {preferencesError}</p>
            ) : preferences ? (
              <form className="space-y-4">
                <div className="flex items-center">
                  <input
                    type="checkbox"
                    id="email_notifications"
                    name="email_notifications"
                    checked={preferences.email_notifications}
                    onChange={handlePreferenceChange}
                    className="h-4 w-4 text-green-600 border-gray-300 rounded focus:ring-green-500"
                  />
                  <label htmlFor="email_notifications" className="ml-2 block text-sm text-gray-900">
                    Email Notifications
                  </label>
                </div>
                <div className="flex items-center">
                  <input
                    type="checkbox"
                    id="in_app_notifications"
                    name="in_app_notifications"
                    checked={preferences.in_app_notifications}
                    onChange={handlePreferenceChange}
                    className="h-4 w-4 text-green-600 border-gray-300 rounded focus:ring-green-500"
                  />
                  <label htmlFor="in_app_notifications" className="ml-2 block text-sm text-gray-900">
                    In-App Notifications
                  </label>
                </div>
                <div className="flex items-center">
                  <input
                    type="checkbox"
                    id="sms_notifications"
                    name="sms_notifications"
                    checked={preferences.sms_notifications}
                    onChange={handlePreferenceChange}
                    className="h-4 w-4 text-green-600 border-gray-300 rounded focus:ring-green-500"
                  />
                  <label htmlFor="sms_notifications" className="ml-2 block text-sm text-gray-900">
                    SMS Notifications
                  </label>
                </div>
                <div className="flex items-center">
                  <input
                    type="checkbox"
                    id="push_notifications"
                    name="push_notifications"
                    checked={preferences.push_notifications}
                    onChange={handlePreferenceChange}
                    className="h-4 w-4 text-green-600 border-gray-300 rounded focus:ring-green-500"
                  />
                  <label htmlFor="push_notifications" className="ml-2 block text-sm text-gray-900">
                    Push Notifications
                  </label>
                </div>
                <Button onClick={handleSavePreferences} className="btn-primary mt-4">Save Preferences</Button>
              </form>
            ) : (
              <p className="text-gray-600">No notification preferences found.</p>
            )}
          </div>
        );
      case 'security':
        return (
          <div>
            <h3 className="text-xl font-semibold mb-4">Two-Factor Authentication</h3>
            {securitySettingsLoading ? (
              <p className="text-gray-600">Loading security settings...</p>
            ) : securitySettingsError ? (
              <p className="text-red-600">Error loading security settings: {securitySettingsError}</p>
            ) : securitySettings ? (
              <div className="space-y-4">
                <div className="flex items-center justify-between bg-gray-50 p-4 rounded-lg">
                  <p className="text-gray-800">2FA Status: <Badge variant={securitySettings.two_factor_enabled ? 'success' : 'default'}>{securitySettings.two_factor_enabled ? 'Enabled' : 'Disabled'}</Badge></p>
                  <Button onClick={handleToggle2FA} variant={securitySettings.two_factor_enabled ? 'destructive' : 'default'}>
                    {securitySettings.two_factor_enabled ? 'Disable 2FA' : 'Enable 2FA'}
                  </Button>
                </div>
              </div>
            ) : (
              <p className="text-gray-600">No security settings found.</p>
            )}

            <h3 className="text-xl font-semibold mt-8 mb-4">Active Login Sessions</h3>
            {sessionsLoading ? (
              <p className="text-gray-600">Loading login sessions...</p>
            ) : sessionsError ? (
              <p className="text-red-600">Error loading login sessions: {sessionsError}</p>
            ) : loginSessions.length === 0 ? (
              <p className="text-gray-500">No active login sessions.</p>
            ) : (
              <div className="overflow-x-auto">
                <Table className="min-w-full bg-white shadow-md rounded-lg overflow-hidden">
                  <TableHeader>
                    <TableRow>
                      <TableHead>Device</TableHead>
                      <TableHead>Location</TableHead>
                      <TableHead>IP Address</TableHead>
                      <TableHead>Last Activity</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead>Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {loginSessions.map((session) => (
                      <TableRow key={session.id}>
                        <TableCell>{session.device}</TableCell>
                        <TableCell>{session.location}</TableCell>
                        <TableCell>{session.ip_address}</TableCell>
                        <TableCell>{new Date(session.last_activity).toLocaleString()}</TableCell>
                        <TableCell>
                          <Badge variant={session.current ? 'success' : 'default'}>
                            {session.current ? 'Current' : 'Active'}
                          </Badge>
                        </TableCell>
                        <TableCell>
                          {!session.current && (
                            <Button variant="destructive" size="sm" onClick={() => handleRevokeSession(session.id)}>
                              Revoke
                            </Button>
                          )}
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            )}
          </div>
        );
      case 'storage-models':
        return (
          <div>
            <h3 className="text-xl font-semibold mb-4">Storage Usage</h3>
            {storageLoading ? (
              <p className="text-gray-600">Loading storage information...</p>
            ) : storageError ? (
              <p className="text-red-600">Error loading storage: {storageError}</p>
            ) : storageInfo ? (
              <div className="space-y-4">
                <div className="bg-gray-50 p-4 rounded-lg">
                  <p className="text-gray-800">Total Space: {storageInfo.total_space_gb} GB</p>
                  <p className="text-gray-800">Used Space: {storageInfo.used_space_gb} GB</p>
                  <p className="text-gray-800">Free Space: {storageInfo.free_space_gb} GB</p>
                  <Progress value={(storageInfo.used_space_gb / storageInfo.total_space_gb) * 100} className="h-2 mt-2" />
                </div>
                <Button onClick={handleClearCache} className="btn-primary">Clear Cache</Button>
              </div>
            ) : (
              <p className="text-gray-600">No storage information found.</p>
            )}

            <h3 className="text-xl font-semibold mt-8 mb-4">Local AI Models</h3>
            {localModelsLoading ? (
              <p className="text-gray-600">Loading local models...</p>
            ) : localModelsError ? (
              <p className="text-red-600">Error loading local models: {localModelsError}</p>
            ) : localModels.length === 0 ? (
              <p className="text-gray-500">No local models found.</p>
            ) : (
              <div className="overflow-x-auto">
                <Table className="min-w-full bg-white shadow-md rounded-lg overflow-hidden">
                  <TableHeader>
                    <TableRow>
                      <TableHead>Name</TableHead>
                      <TableHead>Type</TableHead>
                      <TableHead>Version</TableHead>
                      <TableHead>Size (GB)</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead>Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {localModels.map((model) => (
                      <TableRow key={model.id}>
                        <TableCell>{model.name}</TableCell>
                        <TableCell>{model.type}</TableCell>
                        <TableCell>{model.version}</TableCell>
                        <TableCell>{model.size_gb.toFixed(2)}</TableCell>
                        <TableCell>
                          <Badge variant={model.status === 'installed' ? 'success' : model.status === 'downloading' ? 'info' : 'default'}>
                            {model.status}
                          </Badge>
                          {model.status === 'downloading' && model.download_progress !== undefined && (
                            <Progress value={model.download_progress} className="h-1 mt-1" />
                          )}
                        </TableCell>
                        <TableCell>
                          {model.status === 'available' && (
                            <Button size="sm" onClick={() => handleDownloadModel(model.id)}>Download</Button>
                          )}
                          {model.status === 'installed' && (
                            <Button variant="destructive" size="sm" onClick={() => handleDeleteModel(model.id)}>Delete</Button>
                          )}
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            )}
          </div>
        );
      case 'branding':
        return <BrandingSettingsPage />;
      default:
        return null;
    }
  };

  return (
    <Card className="p-6">
      <h1 className="section-title mb-4">Settings</h1>
      <p className="text-soft-text mb-6">Adjust your application settings.</p>

      <div className="border-b border-gray-200 mb-6">
        <nav className="-mb-px flex space-x-8" aria-label="Tabs">
          <button
            onClick={() => setActiveTab('profile')}
            className={`whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'profile'
                ? 'border-green-500 text-green-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Profile
          </button>
          <button
            onClick={() => setActiveTab('api-integrations')}
            className={`whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'api-integrations'
                ? 'border-green-500 text-green-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            API & Integrations
          </button>
          <button
            onClick={() => setActiveTab('notifications')}
            className={`whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'notifications'
                ? 'border-green-500 text-green-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Notifications
          </button>
          <button
            onClick={() => setActiveTab('security')}
            className={`whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'security'
                ? 'border-green-500 text-green-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Security
          </button>
          <button
            onClick={() => setActiveTab('storage-models')}
            className={`whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'storage-models'
                ? 'border-green-500 text-green-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Storage & Models
          </button>
        <button
            onClick={() => setActiveTab('branding')}
            className={`whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'branding'
                ? 'border-green-500 text-green-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Branding
          </button>
        </nav>
      </div>

      <div>
        {renderContent()}
      </div>
    </Card>
  );
}