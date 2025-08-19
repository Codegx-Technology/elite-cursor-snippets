export interface QuotaItem {
  label: string;
  used: number;
  limit: number;
  unit: string;
}

export interface EnforcementEvent {
  id: string;
  timestamp: string; // ISO string
  type: "slowdown" | "lock" | "view_only" | "quota_warning" | "other";
  message: string;
  details?: any;
}

export interface PlanDashboardData {
  planName: string;
  planCode: string;
  currentStatus: "healthy" | "grace" | "locked" | "view_only" | "slowdown";
  graceExpiresAt?: string; // ISO string, if in grace mode
  quotas: QuotaItem[];
  eventHistory: EnforcementEvent[];
  upgradeUrl: string;
  upgradeNote?: string;
  nextTierComparison?: string; // e.g., "Pro gives you +10k scans & unlocks AI Modules."
}
