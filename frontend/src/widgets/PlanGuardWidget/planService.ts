import type { PlanStatus, PlanEvent } from "./types";

/**
 * Required backend endpoints (implement them on server):
 * GET  /api/plan/status?userId=...    -> returns PlanStatus
 * WS   /ws/plan-events?userId=...     -> streams PlanEvent messages
 * POST /api/plan/upgrade-link         -> returns { url }
 *
 * PlanGuard events are JSON: { id, ts, type, message, payload }
 */

export async function fetchPlanStatus(userId?: string): Promise<PlanStatus> {
  const q = userId ? `?userId=${encodeURIComponent(userId)}` : "";
  const res = await fetch(`/api/plan/status${q}`, { credentials: "include" });
  if (!res.ok) throw new Error("Failed to fetch plan status");
  return res.json() as Promise<PlanStatus>;
}

export function subscribePlanEvents(userId: string | undefined, onEvent: (ev: PlanEvent) => void): WebSocket | null {
  try {
    const url = new URL((process.env.NEXT_PUBLIC_WS_BASE || "ws://localhost:8000") + "/ws/plan-events");
    if (userId) url.searchParams.set("userId", userId);
    const ws = new WebSocket(url.toString());
    ws.onopen = () => console.debug("PlanGuard WS connected");
    ws.onmessage = (m) => {
      try {
        const ev = JSON.parse(m.data) as PlanEvent;
        onEvent(ev);
      } catch (e) {
        console.error("bad event", e);
      }
    };
    ws.onclose = () => console.debug("PlanGuard WS closed");
    return ws;
  } catch (err) {
    console.error("subscribePlanEvents failed", err);
    return null;
  }
}

export function formatDuration(d: Date | null): string {
  if (!d) return "";
  const now = new Date().getTime();
  const diff = Math.max(0, new Date(d).getTime() - now);
  const hrs = Math.floor(diff / (1000 * 60 * 60));
  const mins = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
  return `${hrs}h ${mins}m`;
}