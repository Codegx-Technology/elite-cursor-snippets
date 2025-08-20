/* src/widgets/PlanGuardWidget/planService.ts */
import type { PlanStatus, PlanEvent } from "./types";

const API_BASE = (typeof process !== "undefined" && process.env.NEXT_PUBLIC_API_BASE) || "";

function joinUrl(base: string, path: string) {
  if (!base) return path;
  if (base.endsWith("/") && path.startsWith("/")) return base + path.slice(1);
  if (!base.endsWith("/") && !path.startsWith("/")) return `${base}/${path}`;
  return base + path;
}

function getAuthToken(): string | null {
  if (typeof window === "undefined") return null;
  try {
    return window.localStorage.getItem("access_token");
  } catch {
    return null;
  }
}

export async function fetchPlanStatus(userId?: string): Promise<PlanStatus> {
  const q = userId ? `?userId=${encodeURIComponent(userId)}` : "";
  const url = joinUrl(API_BASE, `/api/plan/status${q}`);
  let res: Response;
  try {
    const token = getAuthToken();
    res = await fetch(url, {
      credentials: "include",
      cache: "no-store",
      headers: {
        Accept: "application/json",
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
    });
  } catch (e) {
    throw new Error(`Network error while fetching plan status from ${url}. Possible CORS/back-end down. ${e instanceof Error ? e.message : String(e)}`);
  }
  if (!res.ok) {
    let body = "";
    try {
      const ct = res.headers.get("content-type") || "";
      if (ct.includes("application/json")) {
        const j = await res.json();
        body = typeof j === "string" ? j : JSON.stringify(j);
      } else {
        body = await res.text();
      }
    } catch (_e) {
      // ignore body parse errors
    }
    throw new Error(`Failed to fetch plan status (${res.status} ${res.statusText}) ${body ? "- " + body : ""}`);
  }
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