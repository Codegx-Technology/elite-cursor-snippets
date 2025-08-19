export type PlanState = "healthy" | "grace" | "view_only" | "locked";

export interface PlanStatus {
  planCode: string;           // "FREE" | "PRO" | "ENTERPRISE"
  planName: string;
  state: PlanState;
  quota: {
    tokens: number;
    audioMins: number;
    videoMins: number;
  };
  usage: {
    tokens: number;
    audioMins: number;
    videoMins: number;
  };
  expiresAt?: string | null;        // iso
  graceExpiresAt?: string | null;   // iso if grace active
  upgradeUrl?: string | null;
  upgradeNote?: string | null;
  upgradeUrlLabel?: string | null;
  // internal diagnostics
  lastCheckedAt?: string | null;
  // admin URLs for tenant-level actions
  adminConsoleUrl?: string | null;
}

export interface PlanEvent {
  id: string;
  ts: string; // ISO
  type: "slowdown" | "lock" | "view_only" | "quota_warning" | "status_change" | "other";
  message: string;
  payload?: any;
}