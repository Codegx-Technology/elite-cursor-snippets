'use client';

import React, { useState } from 'react';
import FormInput from '@/components/FormInput';
import Card from '@/components/Card';

export default function SettingsPage() {
  const [activeTab, setActiveTab] = useState('profile');

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
            <h3 className="text-xl font-semibold mb-4">API & Integrations</h3>
            <p className="text-gray-600">Manage your API keys and third-party integrations here.</p>
            {/* TODO: Implement API key management and integrations UI */}
          </div>
        );
      case 'notifications':
        return (
          <div>
            <h3 className="text-xl font-semibold mb-4">Notification Preferences</h3>
            <p className="text-gray-600">Configure how you receive notifications.</p>
            {/* TODO: Implement notification preferences UI */}
          </div>
        );
      case 'security':
        return (
          <div>
            <h3 className="text-xl font-semibold mb-4">Security Settings</h3>
            <p className="text-gray-600">Enhance your account security.</p>
            {/* TODO: Implement security settings UI (e.g., 2FA, session management) */}
          </div>
        );
      case 'storage-models':
        return (
          <div>
            <h3 className="text-xl font-semibold mb-4">Storage & Local Models</h3>
            <p className="text-gray-600">Manage your storage usage and local AI models.</p>
            {/* TODO: Link to or embed storage/local models management UI */}
          </div>
        );
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
        </nav>
      </div>

      <div>
        {renderContent()}
      </div>
    </Card>
  );
}