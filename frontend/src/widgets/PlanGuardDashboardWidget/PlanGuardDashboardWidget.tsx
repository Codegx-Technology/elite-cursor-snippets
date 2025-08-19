import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress"; // Assuming you have a Progress component
import { fetchPlanDashboardData, formatRemainingTime } from "./dashboardService";
import type { PlanDashboardData, QuotaItem, EnforcementEvent } from "./types";

interface Props {
  userId?: string; // Optional: if widget runs in multi-tenant admin context
}

export default function PlanGuardDashboardWidget({ userId }: Props) {
  const [data, setData] = useState<PlanDashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadData() {
      setLoading(true);
      setError(null);
      try {
        const fetchedData = await fetchPlanDashboardData(userId);
        setData(fetchedData);
      } catch (err: any) {
        console.error("Failed to fetch plan dashboard data:", err);
        setError(err.message || "An unknown error occurred");
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, [userId]);

  if (loading) {
    return (
      <div className="bg-white p-6 rounded-xl shadow-md animate-pulse">
        <div className="h-6 bg-gray-200 rounded w-3/4 mb-4"></div>
        <div className="h-4 bg-gray-200 rounded w-1/2 mb-6"></div>
        <div className="space-y-3">
          <div className="h-4 bg-gray-200 rounded"></div>
          <div className="h-4 bg-gray-200 rounded w-5/6"></div>
          <div className="h-4 bg-gray-200 rounded w-2/3"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 p-6 rounded-xl shadow-md text-red-800">
        <p className="font-semibold">Error loading dashboard:</p>
        <p>{error}</p>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="bg-white p-6 rounded-xl shadow-md">
        <p className="text-gray-600">No plan data available.</p>
      </div>
    );
  }

  const getStatusColor = (status: PlanDashboardData["currentStatus"]) => {
    switch (status) {
      case "healthy":
        return "bg-green-500";
      case "grace":
        return "bg-yellow-500";
      case "slowdown":
        return "bg-orange-500";
      case "view_only":
        return "bg-red-500";
      case "locked":
        return "bg-gray-500";
      default:
        return "bg-gray-400";
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="bg-white p-6 rounded-2xl shadow-xl w-full max-w-3xl mx-auto"
    >
      <div className="flex justify-between items-start mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Your Plan: {data.planName}</h2>
          <p className="text-gray-600">Status: <Badge className={getStatusColor(data.currentStatus)}>{data.currentStatus}</Badge></p>
          {data.currentStatus === "grace" && data.graceExpiresAt && (
            <p className="text-sm text-yellow-700 mt-1">
              Grace period ends in: {formatRemainingTime(data.graceExpiresAt)}
            </p>
          )}
        </div>
        <Button onClick={() => window.open(data.upgradeUrl, "_blank")} className="bg-indigo-600 hover:bg-indigo-700 text-white">
          {data.upgradeNote || "Upgrade Plan"}
        </Button>
      </div>

      {/* Quota Meters */}
      <div className="space-y-4 mb-8">
        <h3 className="text-lg font-semibold text-gray-800">Usage & Limits</h3>
        {data.quotas.map((quota, index) => (
          <QuotaMeter key={index} {...quota} />
        ))}
      </div>

      {/* Event History */}
      <div className="mb-8">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Enforcement History</h3>
        <div className="max-h-60 overflow-y-auto border border-gray-200 rounded-lg p-4 space-y-3">
          {data.eventHistory.length === 0 ? (
            <p className="text-gray-500 text-sm">No enforcement events recorded yet. All good!</p>
          ) : (
            data.eventHistory.map((event, index) => (
              <motion.div
                key={event.id || index}
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: index * 0.05 }}
                className="flex items-start space-x-3 text-sm"
              >
                <div className="text-gray-500 flex-shrink-0">{new Date(event.timestamp).toLocaleString()}:</div>
                <div className="text-gray-800">
                  <span className="font-medium">[{event.type.replace(/_/g, ' ').toUpperCase()}]</span> {event.message}
                </div>
              </motion.div>
            ))
          )}
        </div>
      </div>

      {/* Next Tier Comparison */}
      {data.nextTierComparison && (
        <div className="bg-blue-50 border-l-4 border-blue-400 text-blue-800 p-4 rounded-lg" role="alert">
          <p className="font-bold">Unlock More!</p>
          <p>{data.nextTierComparison}</p>
        </div>
      )}
    </motion.div>
  );
}

// Sub-component for Quota Meter
function QuotaMeter({ label, used, limit, unit }: QuotaItem) {
  const percentage = limit > 0 ? (used / limit) * 100 : 0;
  const displayPercentage = Math.min(100, percentage);

  let progressColor = "bg-green-500";
  if (percentage > 75) progressColor = "bg-yellow-500";
  if (percentage > 90) progressColor = "bg-red-500";

  return (
    <div>
      <div className="flex justify-between text-sm font-medium text-gray-700 mb-1">
        <span>{label}</span>
        <span>
          {used} / {limit} {unit}
        </span>
      </div>
      <Progress value={displayPercentage} className={`h-2 ${progressColor}`} />
    </div>
  );
}
