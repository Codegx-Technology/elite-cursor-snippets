import React, { useEffect, useState } from "react";
import SuperAdminCard from "./SuperAdminCard";
import UserManagementSection from './UserManagementSection';
import TenantManagementSection from './TenantManagementSection';
import TTSVoiceManagementSection from './TTSVoiceManagementSection';
import { apiClient, SuperAdminMetrics } from '@/lib/api'; // Import apiClient and SuperAdminMetrics

interface SuperAdminDashboardProps {
  userRole: string;
}

const SuperAdminDashboard: React.FC<SuperAdminDashboardProps> = ({ userRole }) => {
  const [metrics, setMetrics] = useState<SuperAdminMetrics | null>(null);

  useEffect(() => {
    if (userRole === "admin" || userRole === "superadmin") {
      // Mock metrics for development when backend is not available
      const mockMetrics: SuperAdminMetrics = {
        total_users: 1247,
        active_users: 892,
        total_tenants: 15,
        active_tenants: 12,
        total_videos_generated: 15640,
        total_storage_used: "2.3 TB",
        system_health: "healthy",
        pending_approvals: 3
      };

      apiClient.getSuperAdminMetrics().then((response: any) => {
        if (response.data) {
          setMetrics(response.data);
        } else if (response.error) {
          console.warn("Backend not available, using mock metrics:", response.error);
          setMetrics(mockMetrics);
        }
      }).catch(() => {
        console.warn("Backend not available, using mock metrics");
        setMetrics(mockMetrics);
      });
    }
  }, [userRole]);

  if (userRole !== "admin" && userRole !== "superadmin") return null; // hide for non-admins

  return (
    <div className="superadmin-dashboard p-4">
      <h2 className="text-2xl font-bold mb-4">SuperAdmin Dashboard</h2>
      {metrics ? (
        <SuperAdminCard metrics={metrics} />
      ) : (
        <p>Loading metrics...</p>
      )}

      <div className="mt-8">
        <h3 className="text-xl font-bold mb-4">User Management</h3>
        <UserManagementSection />
      </div>

      <div className="mt-8">
        <h3 className="text-xl font-bold mb-4">Tenant Management</h3>
        <TenantManagementSection />
      </div>

      <div className="mt-8">
        <h3 className="text-xl font-bold mb-4">TTS Voice Management</h3>
        <TTSVoiceManagementSection />
      </div>
    </div>
  );
};

export default SuperAdminDashboard;
