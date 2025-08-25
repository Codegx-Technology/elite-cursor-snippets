'use client';

import { useApiIntegration } from '@/hooks/useApiIntegration';
import { FaSpinner, FaPlus, FaTrash } from 'react-icons/fa6';
import Card from '@/components/Card';

// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorclean
// [CONTEXT]: Reusable API Integration component
// [GOAL]: Provide a clean and reusable component for managing API keys and integrations

export default function ApiIntegration() {
  const { apiKeys, integrations, isLoading, error, generateApiKey, revokeApiKey, updateIntegration } = useApiIntegration();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <FaSpinner className="w-8 h-8 text-green-600 animate-spin mx-auto mb-4" />
          <span className="text-gray-600 font-medium">Loading API integration data...</span>
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
      <h1 className="section-title text-center mb-8">API & Integration Management</h1>

      <Card className="p-6 mb-6">
        <h2 className="text-xl font-bold text-gray-800 mb-4">API Keys</h2>
        <button onClick={generateApiKey} className="btn-primary px-4 py-2 rounded-lg flex items-center space-x-2 mb-4">
          <FaPlus />
          <span>Generate New API Key</span>
        </button>

        {apiKeys.length === 0 ? (
          <div className="text-center text-soft-text">
            <p>No API keys found. Generate one to get started.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full bg-white rounded-lg shadow-md">
              <thead>
                <tr className="bg-gray-100 text-left text-soft-text text-sm font-medium uppercase tracking-wider">
                  <th className="py-3 px-4 rounded-tl-lg">Key</th>
                  <th className="py-3 px-4">Created At</th>
                  <th className="py-3 px-4">Last Used At</th>
                  <th className="py-3 px-4">Status</th>
                  <th className="py-3 px-4 rounded-tr-lg">Actions</th>
                </tr>
              </thead>
              <tbody>
                {apiKeys.map((key) => (
                  <tr key={key.id} className="border-b border-gray-200 hover:bg-gray-50">
                    <td className="py-3 px-4 text-charcoal line-clamp-1">{key.key}</td>
                    <td className="py-3 px-4 text-charcoal">{new Date(key.created_at).toLocaleDateString()}</td>
                    <td className="py-3 px-4 text-charcoal">{key.last_used_at ? new Date(key.last_used_at).toLocaleDateString() : 'Never'}</td>
                    <td className="py-3 px-4">
                      <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${key.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                        {key.is_active ? 'Active' : 'Revoked'}
                      </span>
                    </td>
                    <td className="py-3 px-4">
                      <button onClick={() => revokeApiKey(key.id)} className="text-red-600 hover:text-red-900 text-sm">
                        <FaTrash /> Revoke
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>

      <Card className="p-6 mt-6">
        <h2 className="text-xl font-bold text-gray-800 mb-4">Integrations</h2>
        {integrations.length === 0 ? (
          <div className="text-center text-soft-text">
            <p>No integrations configured.</p>
          </div>
        ) : (
          <div className="space-y-4">
            {integrations.map((integration) => (
              <div key={integration.id} className="border border-gray-200 p-4 rounded-lg flex justify-between items-center">
                <div>
                  <h3 className="font-medium text-gray-800">{integration.name} ({integration.type})</h3>
                  <p className="text-sm text-gray-600">Status: {integration.is_enabled ? 'Enabled' : 'Disabled'}</p>
                </div>
                <button onClick={() => updateIntegration(integration.id, { is_enabled: !integration.is_enabled })} className="btn-secondary px-4 py-2 rounded-lg">
                  {integration.is_enabled ? 'Disable' : 'Enable'}
                </button>
              </div>
            ))}
          </div>
        )}
      </Card>
    </div>
  );
}
