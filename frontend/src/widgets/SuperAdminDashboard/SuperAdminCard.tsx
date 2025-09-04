import React from "react";

import { SuperAdminMetrics } from '@/lib/api';

interface SuperAdminCardProps {
  metrics: SuperAdminMetrics;
}

const SuperAdminCard: React.FC<SuperAdminCardProps> = ({ metrics }) => {
  return (
    <div className="superadmin-card bg-white p-4 rounded shadow">
      <pre>{JSON.stringify(metrics, null, 2)}</pre>
    </div>
  );
};

export default SuperAdminCard;
