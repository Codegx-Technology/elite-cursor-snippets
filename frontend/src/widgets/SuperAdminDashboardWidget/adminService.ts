// frontend/src/widgets/SuperAdminDashboardWidget/adminService.ts

import { apiClient, handleApiResponse } from "@/lib/api";
import type { UserData, Tenant, AuditLogEntry } from "@/lib/api";

const API_BASE = (typeof process !== "undefined" && process.env.NEXT_PUBLIC_API_BASE) || "";

// Mock data for development when backend is not available
const mockUsers: UserData[] = [
  {
    id: 1,
    username: "admin",
    email: "admin@shujaa.studio",
    role: "admin",
    tenant_name: "ShujaaStudio",
    is_active: true
  },
  {
    id: 2, 
    username: "johndoe",
    email: "user1@example.com",
    role: "user",
    tenant_name: "Example Corp",
    is_active: true
  },
  {
    id: 3,
    username: "janesmith",
    email: "user2@example.com", 
    role: "user",
    tenant_name: "Demo Company",
    is_active: false
  }
];

export async function fetchAllUsers(): Promise<UserData[]> {
  // Use mock data when backend is not available
  if (!API_BASE || API_BASE === "") {
    console.warn("No API_BASE configured, using mock user data");
    return Promise.resolve(mockUsers);
  }

  try {
    const response = await apiClient.getSuperAdminUsers();
    return new Promise((resolve, reject) => {
      handleApiResponse(
        response,
        (data) => resolve(data),
        (error) => reject(new Error(error))
      );
    });
  } catch (error) {
    console.warn("Backend not available, using mock user data:", error);
    return Promise.resolve(mockUsers);
  }
}

// Mock tenants data
const mockTenants: Tenant[] = [
  {
    id: 1,
    name: "ShujaaStudio",
    is_active: true,
    plan: "Enterprise"
  },
  {
    id: 2,
    name: "Example Corp",
    is_active: true,
    plan: "Professional"
  },
  {
    id: 3,
    name: "Demo Company",
    is_active: false,
    plan: "Free"
  }
];

export async function fetchAllTenants(): Promise<Tenant[]> {
  // Use mock data when backend is not available
  if (!API_BASE || API_BASE === "") {
    console.warn("No API_BASE configured, using mock tenant data");
    return Promise.resolve(mockTenants);
  }

  try {
    const response = await apiClient.getSuperAdminTenants();
    return new Promise((resolve, reject) => {
      handleApiResponse(
        response,
        (data) => {
          // Map Tenant data to include 'plan' field, which is not directly from backend for now
          const mappedTenants: Tenant[] = data.map((tenant: Tenant) => ({
            id: tenant.id,
            name: tenant.name,
            is_active: tenant.is_active,
            plan: tenant.plan || "Free", // Placeholder for plan, as it's not directly returned by backend yet
          }));
          resolve(mappedTenants);
        },
        (error) => reject(new Error(error))
      );
    });
  } catch (error) {
    console.warn("Backend not available, using mock tenant data:", error);
    return Promise.resolve(mockTenants);
  }
}

// Mock audit logs data
const mockAuditLogs: AuditLogEntry[] = [
  {
    id: "1",
    timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
    event_type: "USER_LOGIN",
    message: "Admin user logged in successfully",
    user_id: "1"
  },
  {
    id: "2",
    timestamp: new Date(Date.now() - 4 * 60 * 60 * 1000).toISOString(),
    event_type: "VIDEO_GENERATED",
    message: "User generated new video content",
    user_id: "2"
  },
  {
    id: "3",
    timestamp: new Date(Date.now() - 6 * 60 * 60 * 1000).toISOString(),
    event_type: "TENANT_CREATED",
    message: "New tenant 'Demo Company' was created",
    user_id: "1"
  },
  {
    id: "4",
    timestamp: new Date(Date.now() - 12 * 60 * 60 * 1000).toISOString(),
    event_type: "USER_DEACTIVATED",
    message: "User account was deactivated",
    user_id: "3"
  }
];

export async function fetchAuditLogs(): Promise<AuditLogEntry[]> {
  // Use mock data when backend is not available
  if (!API_BASE || API_BASE === "") {
    console.warn("No API_BASE configured, using mock audit log data");
    return Promise.resolve(mockAuditLogs);
  }

  try {
    const response = await apiClient.getSuperAdminAuditLogs();
    return new Promise((resolve, reject) => {
      handleApiResponse(
        response,
        (data) => resolve(data),
        (error) => reject(new Error(error))
      );
    });
  } catch (error) {
    console.warn("Backend not available, using mock audit log data:", error);
    return Promise.resolve(mockAuditLogs);
  }
}