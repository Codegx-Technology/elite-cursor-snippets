import React, { useEffect, useState, useRef } from "react";
import { motion } from "framer-motion";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { fetchPlanStatus, subscribePlanEvents, formatDuration } from "./planService";
import type { PlanStatus, PlanEvent } from "./types";
import ViewOnlyOverlay from "@/components/PlanGuard/ViewOnlyOverlay";

type Props = {
  userId?: string;
  pollIntervalMs?: number;
  showUpgradeBtn?: boolean;
  theme?: "default" | "compact";
  isRestricted?: boolean; // New prop to indicate if the widget is in a restricted state
};

export default function PlanGuardWidget({
  userId,
  pollIntervalMs = 30000,
  showUpgradeBtn = true,
  theme = "default",
  isRestricted = false, // Destructure and provide a default value
}: Props) {
  const [status, setStatus] = useState<PlanStatus | null>(null);
  const [events, setEvents] = useState<PlanEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    let mounted = true;
    async function load() {
      setLoading(true);
      try {
        const s = await fetchPlanStatus(userId);
        if (!mounted) return;
        setStatus(s);
      } catch (err) {
        console.error("PlanGuardWidget: fetchPlanStatus failed", err);
      } finally {
        if (mounted) setLoading(false);
      }
    }
    load();
    const poll = setInterval(load, pollIntervalMs);
    return () => {
      mounted = false;
      clearInterval(poll);
    };
  }, [userId, pollIntervalMs]);

  useEffect(() => {
    const ws = subscribePlanEvents(userId, (ev) => {
      setEvents((prev) => [ev, ...prev].slice(0, 50));
      if (ev.type === "status_change" && ev.payload?.status) {
        setStatus(ev.payload.status as PlanStatus);
      }
    });
    wsRef.current = ws;
    return () => {
      if (wsRef.current) wsRef.current.close();
    };
  }, [userId]);

  if (loading) {
    return (
      <div className="bg-white p-4 rounded-xl shadow-sm w-full">
        <div className="animate-pulse h-6 bg-gray-100 rounded w-1/3 mb-3" />
        <div className="h-24 bg-gray-50 rounded" />
      </div>
    );
  }

  if (!status) {
    return (
      <div className="bg-white p-4 rounded-xl shadow-sm">
        <p className="text-sm text-gray-600">Plan information unavailable</p>
      </div>
    );
  }

  const remaining = status.graceExpiresAt ? formatDuration(new Date(status.graceExpiresAt)) : null;
  const isGrace = status.state === "grace";
  const isViewOnly = status.state === "view_only";

  return (
    <div className={`bg-white rounded-2xl p-4 shadow-md ${theme === "compact" ? "max-w-md" : "w-full"}`}>
      <div className="flex items-start justify-between gap-4">
        <div>
          <h3 className="text-lg font-semibold">Usage & Limits</h3>
          <p className="text-sm text-gray-500">Plan: <span className="font-medium">{status.planName}</span></p>
        </div>

        <div className="flex items-center gap-3">
          <Badge>{status.planCode}</Badge>
          {isGrace && (
            <div className="text-sm text-yellow-700 bg-yellow-50 px-2 py-1 rounded">
              Grace: {remaining}
            </div>
          )}
          {isViewOnly && <div className="text-sm text-red-700 bg-red-50 px-2 py-1 rounded">View-Only</div>}
        </div>
      </div>

      <div className="mt-4 space-y-3">
        <QuotaBar label="API Calls (monthly)" used={status.usage.tokens} limit={status.quota.tokens} />
        <QuotaBar label="Audio (mins)" used={status.usage.audioMins} limit={status.quota.audioMins} />
        <QuotaBar label="Video (mins)" used={status.usage.videoMins} limit={status.quota.videoMins} />
      </div>

      <div className="mt-4">
        <div className="flex items-center justify-between">
          <h4 className="text-sm font-medium">Recent enforcement events</h4>
          {showUpgradeBtn && (
            <Button
              variant="ghost"
              onClick={() => window.open(status.upgradeUrl || "/billing", "_blank")}
              disabled={isRestricted} // Disable if restricted
            >
              Upgrade
            </Button>
          )}
        </div>

        <div className="mt-2 max-h-40 overflow-y-auto space-y-2">
          {events.length === 0 && <p className="text-sm text-gray-400">No events yet</p>}
          {events.map((ev) => (
            <motion.div
              key={ev.id}
              initial={{ opacity: 0, y: -6 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex items-start gap-3 p-2 rounded hover:bg-gray-50"
            >
              <div className="text-xs text-gray-500">{new Date(ev.ts).toLocaleString()}</div>
              <div className="text-sm text-gray-700">{ev.message}</div>
            </motion.div>
          ))}
        </div>
      </div>

      {isViewOnly && status.graceExpiresAt && (
        <ViewOnlyOverlay
          expiredAt={new Date(status.expiresAt || status.graceExpiresAt).toLocaleString()}
          onUpgrade={() => window.open(status.upgradeUrl || "/billing", "_blank")}
        />
      )}
    </div>
  );
}

function QuotaBar({ label, used, limit }: { label: string; used: number; limit: number }) {
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
}
