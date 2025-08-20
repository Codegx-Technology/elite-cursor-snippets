/* src/widgets/PlanGuardWidget/types.ts */
export type PlanState = "healthy" | "grace" | "view_only" | "locked";

export interface PlanStatus {
  planCode: string;
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
  expiresAt?: string | null;
  graceExpiresAt?: string | null;
  upgradeUrl?: string | null;
  lastCheckedAt?: string | null;
  adminConsoleUrl?: string | null;
}
export interface PlanEvent {
  id: string;
  ts: string;
  type: "slowdown" | "lock" | "view_only" | "quota_warning" | "status_change" | "other";
  message: string;
  payload?: any;
}