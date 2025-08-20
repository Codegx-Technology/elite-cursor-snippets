import React, { useEffect, useState } from "react";
import SuperAdminCard from "./SuperAdminCard";
import { getSuperAdminMetrics } from "../../../api/superadmin";

interface SuperAdminDashboardProps {
  userRole: string;
}

const SuperAdminDashboard: React.FC<SuperAdminDashboardProps> = ({ userRole }) => {
  const [metrics, setMetrics] = useState<any>(null);

  useEffect(() => {
    if (userRole === "superadmin") {
      getSuperAdminMetrics().then(setMetrics);
    }
  }, [userRole]);

  if (userRole !== "superadmin") return null; // hide for non-superadmins

  import UserManagementSection from './UserManagementSection'; // New import
import TenantManagementSection from './TenantManagementSection'; // New import
import TTSVoiceManagementSection from './TTSVoiceManagementSection'; // New import

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
