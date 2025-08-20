/* src/widgets/PlanGuardWidget/planService.ts */
import type { PlanStatus, PlanEvent } from "./types";

export async function fetchPlanStatus(userId?: string): Promise<PlanStatus> {
  const q = userId ? `?userId=${encodeURIComponent(userId)}` : "";
  const res = await fetch(`/api/plan/status${q}`, { credentials: "include" });
  if (!res.ok) throw new Error("Failed to fetch plan status");
  return res.json() as Promise<PlanStatus>;
}

export function subscribePlanEvents(userId: string | undefined, onEvent: (ev: PlanEvent) => void): WebSocket | null {
  try {
    const base = process.env.NEXT_PUBLIC_WS_BASE || (typeof window !== "undefined" ? window.location.origin.replace(/^http/, "ws") : "ws://localhost:3000");
    const url = new URL(`${base}/ws/plan-events`);
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