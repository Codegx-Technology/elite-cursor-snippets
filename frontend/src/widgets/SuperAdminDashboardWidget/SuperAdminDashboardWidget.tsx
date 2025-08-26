import React from 'react';
import UserManagementSection from '../SuperAdminDashboard/UserManagementSection';
import TenantManagementSection from '../SuperAdminDashboard/TenantManagementSection';
import AuditLogSection from '../SuperAdminDashboard/AuditLogSection';

interface Props {
  userId?: string;
}

export default function SuperAdminDashboardWidget({ userId }: Props) {
  return (
    <div className="bg-white p-6 rounded-xl shadow-md">
      <h2 className="text-2xl font-bold mb-4">Super Admin Dashboard</h2>
      <p className="text-gray-600">Welcome, Super Admin! User ID: {userId}</p>

      <div className="mt-6 space-y-4">
        <UserManagementSection />

        <TenantManagementSection />

        <h3 className="text-xl font-semibold">PlanGuard Control</h3>
        <ul className="list-disc list-inside ml-4">
          <li>Global PlanGuard override switch (TODO)</li>
          <li>Force downgrade / upgrade tenants (TODO)</li>
          <li>View all grace-period expirations (TODO)</li>
          <li>Dependency enforcement monitor (TODO)</li>
        </ul>

        <h3 className="text-xl font-semibold">Widget Registry Oversight</h3>
        <ul className="list-disc list-inside ml-4">
          <li>Approve / remove widgets from marketplace (TODO)</li>
          <li>Global widget updates (TODO)</li>
          <li>Dependency lock management (TODO)</li>
          <li>Audit logs of widget installs/updates (TODO)</li>
        </ul>

        <h3 className="text-xl font-semibold">Analytics & Monitoring</h3>
        <ul className="list-disc list-inside ml-4">
          <li>Active users per tenant (TODO)</li>
          <li>Widget usage stats (per tenant & global) (TODO)</li>
          <li>Billing usage (API calls, limits, overages) (TODO)</li>
          <li>Error / crash reports (TODO)</li>
        </ul>

        <h3 className="text-xl font-semibold">System Config</h3>
        <ul className="list-disc list-inside ml-4">
          <li>Toggle experimental features (TODO)</li>
          <li>Global branding (logo, theme, color) (TODO)</li>
          <li>Backup & restore configs (TODO)</li>
        </ul>

        <AuditLogSection />

        <h3 className="text-xl font-semibold">Security</h3>
        <ul className="list-disc list-inside ml-4">
          <li>Manage API keys / secrets per tenant (TODO)</li>
          <li>Set password policies (TODO)</li>
          <li>Global session invalidation (TODO)</li>
        </ul>

        <h3 className="text-xl font-semibold">Support</h3>
        <ul className="list-disc list-inside ml-4">
          <li>Ticket system (view + reassign tenant support requests) (TODO)</li>
          <li>Impersonate tenant admin for debugging (TODO)</li>
        </ul>
      </div>
    </div>
  );
}
