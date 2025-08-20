// frontend/src/widgets/UserPlanDashboard/index.tsx

"use client";

import React, { useEffect, useState } from 'react';
import { useAuth } from '@/context/AuthContext';
import { getCurrentPlan } from '@/core/planGuard';
import UsageMeter from './UsageMeter';
import EventTimeline from './EventTimeline';
import UpgradeCTA from './UpgradeCTA';
import { PlanMessages } from '@/ui/planMessages';

export default function UserPlanDashboardWidget() {
  const { user, isAuthenticated, isLoading } = useAuth();
  const [planInfo, setPlanInfo] = useState<any>(null);
  const [loadingPlan, setLoadingPlan] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPlan = async () => {
      if (isAuthenticated && user) {
        setLoadingPlan(true);
        setError(null);
        try {
          const currentPlan = await getCurrentPlan({ userId: user.id, userRole: user.role });
          setPlanInfo(currentPlan);
        } catch (err: any) {
          console.error("Failed to fetch user plan:", err);
          setError(err.message || "Failed to load plan information.");
        } finally {
          setLoadingPlan(false);
        }
      } else if (!isLoading) {
        setLoadingPlan(false);
        setError("Not authenticated.");
      }
    };

    fetchPlan();
  }, [isAuthenticated, user, isLoading]);

  if (loadingPlan) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <span className="text-gray-600 font-medium">Loading plan details...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
        <strong className="font-bold">Error:</strong>
        <span className="block sm:inline"> {error}</span>
      </div>
    );
  }

  if (!planInfo) {
    return (
      <div className="bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-3 rounded relative" role="alert">
        <strong className="font-bold">Warning:</strong>
        <span className="block sm:inline"> Plan information not available.</span>
      </div>
    );
  }

  // Determine current plan state for messages
  const isGrace = planInfo.tier.includes("Grace");
  const isFallback = planInfo.tier.includes("Fallback");

  return (
    <div className="space-y-6 p-4">
      <h1 className="text-3xl font-bold text-gray-900">Your Plan & Usage</h1>

      {isGrace && (
        <div className="bg-yellow-50 border-l-4 border-yellow-500 text-yellow-700 p-4" role="alert">
          <p className="font-bold">{PlanMessages.GRACE_PERIOD_ACTIVE}</p>
          <p className="text-sm">{PlanMessages.GRACE_PERIOD_WARNING}</p>
        </div>
      )}

      {isFallback && (
        <div className="bg-orange-50 border-l-4 border-orange-500 text-orange-700 p-4" role="alert">
          <p className="font-bold">{PlanMessages.API_DOWN_LIMITED_MODE}</p>
          <p className="text-sm">Some features may be restricted.</p>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <UsageMeter planInfo={planInfo} />
        <EventTimeline /> {/* This will fetch its own events */}
      </div>

      <UpgradeCTA planInfo={planInfo} />
    </div>
  );
}
