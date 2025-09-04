// frontend/src/widgets/UserPlanDashboard/UsageMeter.tsx

import React from 'react';
import { Entitlement } from '@/core/planGuard';
import { PlanMessages } from '@/ui/planMessages';

interface UsageMeterProps {
  planInfo: { tier: string; entitlements: Entitlement[] };
}

const UsageMeter: React.FC<UsageMeterProps> = ({ planInfo }) => {
  const getQuotaProgress = (key: string) => {
    const entitlement = planInfo.entitlements.find(e => e.key === key);
    if (!entitlement || !entitlement.limits) return { used: 0, limit: 0, pct: 0 };

    // Assuming limits are simple numbers for now
    const limit = entitlement.limits[key] || 0; // Use key as the limit property name
    const used = 0; // TODO: Fetch actual usage from backend
    const pct = limit > 0 ? Math.min(100, Math.round((used / limit) * 100)) : 0;
    return { used, limit, pct };
  };

  const videoQuota = getQuotaProgress('video_generation');
  const audioQuota = getQuotaProgress('audio_generation');
  const apiQuota = getQuotaProgress('api_calls');

  return (
    <div className="bg-white p-6 rounded-lg shadow-md space-y-4">
      <h2 className="text-xl font-semibold text-gray-800">Usage & Limits</h2>
      <p className="text-gray-600">Current Plan: <span className="font-bold">{planInfo.tier}</span></p>

      <div className="space-y-3">
        {/* Video Quota */}
        <QuotaBar label="Video Generation (mins)" used={videoQuota.used} limit={videoQuota.limit} />
        {/* Audio Quota */}
        <QuotaBar label="Audio Generation (mins)" used={audioQuota.used} limit={audioQuota.limit} />
        {/* API Calls Quota */}
        <QuotaBar label="API Calls (tokens)" used={apiQuota.used} limit={apiQuota.limit} />
      </div>

      {/* Smart Upsell Nudges */}
      {planInfo.tier.toLowerCase().includes('free') && (
        <p className="text-sm text-gray-500 mt-4">
          {PlanMessages.UPSELL_NUDGE_FREE_TO_PRO}
        </p>
      )}
      {planInfo.tier.toLowerCase().includes('pro') && (
        <p className="text-sm text-gray-500 mt-4">
          {PlanMessages.UPSELL_NUDGE_PRO_TO_ENTERPRISE}
        </p>
      )}
    </div>
  );
};

const QuotaBar: React.FC<{ label: string; used: number; limit: number }> = ({ label, used, limit }) => {
  const pct = limit > 0 ? Math.min(100, Math.round((used / limit) * 100)) : 0;
  const color = pct < 60 ? "bg-emerald-500" : pct < 90 ? "bg-yellow-400" : "bg-red-500";

  return (
    <div>
      <div className="flex justify-between text-xs text-gray-500">
        <div>{label}</div>
        <div>{used}/{limit}</div>
      </div>
      <div className="w-full h-2 bg-gray-100 rounded mt-1">
        <div className={`${color} h-2 rounded`} style={{ width: `${pct}%` }} />
      </div>
    </div>
  );
};

export default UsageMeter;
