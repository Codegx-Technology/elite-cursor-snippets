import type { PlanDashboardData } from "./types";

/**
 * Required backend endpoints for the PlanGuard Dashboard Widget:
 * GET /api/user/plan-dashboard?userId=... -> returns PlanDashboardData
 * WS /ws/user-plan-events?userId=...     -> streams EnforcementEvent messages (optional, for real-time updates)
 */

export async function fetchPlanDashboardData(userId?: string): Promise<PlanDashboardData> {
  const q = userId ? `?userId=${encodeURIComponent(userId)}` : "";
  const res = await fetch(`/api/user/plan-dashboard${q}`, { credentials: "include" });
  if (!res.ok) throw new Error("Failed to fetch plan dashboard data");
  return res.json() as Promise<PlanDashboardData>;
}

// Optional: WebSocket for real-time updates
export function subscribeUserPlanEvents(userId: string | undefined, onEvent: (ev: EnforcementEvent) => void): WebSocket | null {
  try {
    const base = process.env.NEXT_PUBLIC_WS_BASE || (typeof window !== "undefined" ? window.location.origin.replace(/^http/, "ws") : "ws://localhost:3000");
    const url = new URL(`${base}/ws/user-plan-events`);
    if (userId) url.searchParams.set("userId", userId);
    const ws = new WebSocket(url.toString());
    ws.onopen = () => console.debug("User Plan WS connected");
    ws.onmessage = (m) => {
      try {
        const ev = JSON.parse(m.data);
        onEvent(ev);
      } catch (e) {
        console.error("bad user plan event", e);
      }
    };
    ws.onclose = () => console.debug("User Plan WS closed");
    return ws;
  } catch (err) {
    console.error("subscribeUserPlanEvents failed", err);
    return null;
  }
}

export function formatRemainingTime(graceExpiresAt: string): string {
  const now = new Date().getTime();
  const expirationDate = new Date(graceExpiresAt).getTime();
  const diff = Math.max(0, expirationDate - now);

  const hours = Math.floor(diff / (1000 * 60 * 60));
  const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
  const seconds = Math.floor((diff % (1000 * 60)) / 1000);

  if (hours > 0) {
    return `${hours}h ${minutes}m`;
  } else if (minutes > 0) {
    return `${minutes}m ${seconds}s`;
  } else {
    return `${seconds}s`;
  }
}
