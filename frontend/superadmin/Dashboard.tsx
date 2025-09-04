// frontend/superadmin/Dashboard.tsx

"use client";

import React, { useState } from 'react';
import Link from 'next/link';
import { useAuth } from '@/context/AuthContext';
import { useRouter } from 'next/navigation';

// Placeholder components for each section
const TenantsSection = () => <div className="p-6 bg-white rounded-lg shadow">Tenant Management Content (TODO)</div>;
const UsersSection = () => <div className="p-6 bg-white rounded-lg shadow">User Management Content (TODO)</div>;
const WidgetsSection = () => <div className="p-6 bg-white rounded-lg shadow">Widget Marketplace Approvals Content (TODO)</div>;
const PlansSection = () => <div className="p-6 bg-white rounded-lg shadow">Plan Management Content (TODO)</div>;
const SystemHealthSection = () => <div className="p-6 bg-white rounded-lg shadow">System Health Metrics Content (TODO)</div>;
const DependenciesSection = () => <div className="p-6 bg-white rounded-lg shadow">Global Dependency Monitor Content (TODO)</div>;

const SuperAdminDashboard: React.FC = () => {
  const { user, isAuthenticated, isLoading, logout } = useAuth();
  const router = useRouter();
  const [activeSection, setActiveSection] = useState('tenants'); // Default active section

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <span className="text-gray-600 font-medium">Loading authentication...</span>
        </div>
      </div>
    );
  }

  if (!isAuthenticated || user?.role !== 'admin') {
    router.push('/login');
    return null;
  }

  const renderSection = () => {
    switch (activeSection) {
      case 'tenants': return <TenantsSection />;
      case 'users': return <UsersSection />;
      case 'widgets': return <WidgetsSection />;
      case 'plans': return <PlansSection />;
      case 'health': return <SystemHealthSection />;
      case 'dependencies': return <DependenciesSection />;
      default: return <TenantsSection />;
    }
  };

  return (
    <div className="flex min-h-screen bg-gray-100">
      {/* Sidebar */}
      <aside className="w-64 bg-gray-800 text-white p-6 space-y-6">
        <h2 className="text-2xl font-bold mb-6">Super Admin</h2>
        <nav>
          <ul className="space-y-2">
            <li>
              <a
                href="#tenants"
                onClick={() => setActiveSection('tenants')}
                className={`block py-2 px-4 rounded transition duration-200 ${activeSection === 'tenants' ? 'bg-gray-700' : 'hover:bg-gray-700'}`}
              >
                Tenants
              </a>
            </li>
            <li>
              <a
                href="#users"
                onClick={() => setActiveSection('users')}
                className={`block py-2 px-4 rounded transition duration-200 ${activeSection === 'users' ? 'bg-gray-700' : 'hover:bg-gray-700'}`}
              >
                Users
              </a>
            </li>
            <li>
              <a
                href="#widgets"
                onClick={() => setActiveSection('widgets')}
                className={`block py-2 px-4 rounded transition duration-200 ${activeSection === 'widgets' ? 'bg-gray-700' : 'hover:bg-gray-700'}`}
              >
                Widgets
              </a>
            </li>
            <li>
              <a
                href="#plans"
                onClick={() => setActiveSection('plans')}
                className={`block py-2 px-4 rounded transition duration-200 ${activeSection === 'plans' ? 'bg-gray-700' : 'hover:bg-gray-700'}`}
              >
                Plans
              </a>
            </li>
            <li>
              <a
                href="#health"
                onClick={() => setActiveSection('health')}
                className={`block py-2 px-4 rounded transition duration-200 ${activeSection === 'health' ? 'bg-gray-700' : 'hover:bg-gray-700'}`}
              >
                System Health
              </a>
            </li>
            <li>
              <a
                href="#dependencies"
                onClick={() => setActiveSection('dependencies')}
                className={`block py-2 px-4 rounded transition duration-200 ${activeSection === 'dependencies' ? 'bg-gray-700' : 'hover:bg-gray-700'}`}
              >
                Dependencies
              </a>
            </li>
          </ul>
        </nav>
        <button
          onClick={logout}
          className="w-full py-2 px-4 bg-red-600 hover:bg-red-700 rounded transition duration-200"
        >
          Logout
        </button>
      </aside>

      {/* Main content area */}
      <main className="flex-1 p-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Super Admin Dashboard</h1>
        {renderSection()}
      </main>
    </div>
  );
};

export default SuperAdminDashboard;
