// frontend/src/widgets/SuperAdminDashboardWidget/types.ts

export interface UserData {
  id: number;
  username: string;
  email: string;
  role: string;
  tenant_name: string;
  is_active: boolean;
}

export interface TenantData {
  id: number;
  name: string;
  plan: string;
  is_active: boolean;
  // Add more tenant-related fields as needed
}

export interface PlanData {
  name: string;
  description: string;
  price: number;
  // Add more plan-related fields as needed
}

export interface AuditLogEntry {
  id: number;
  timestamp: string;
  event_type: string;
  message: string;
  // Add more audit log fields as needed
}

// Add more interfaces for other admin-related data models
