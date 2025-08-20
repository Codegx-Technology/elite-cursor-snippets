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

  return (
    <div className="superadmin-dashboard p-4">
      <h2 className="text-2xl font-bold mb-4">SuperAdmin Dashboard</h2>
      {metrics ? (
        <SuperAdminCard metrics={metrics} />
      ) : (
        <p>Loading metrics...</p>
      )}
    </div>
  );
};

export default SuperAdminDashboard;
