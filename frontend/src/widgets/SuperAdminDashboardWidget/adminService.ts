// frontend/src/widgets/SuperAdminDashboardWidget/adminService.ts

import { apiClient, handleApiResponse } from "@/lib/api";
import type { UserData, Tenant, AuditLogEntry } from "@/lib/api";

export async function fetchAllUsers(): Promise<UserData[]> {
  const response = await apiClient.getSuperAdminUsers();
  return new Promise((resolve, reject) => {
    handleApiResponse(
      response,
      (data) => resolve(data),
      (error) => reject(new Error(error))
    );
  });
}

export async function fetchAllTenants(): Promise<Tenant[]> {
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
}

export async function fetchAuditLogs(): Promise<AuditLogEntry[]> {
    const response = await apiClient.getSuperAdminAuditLogs();
    return new Promise((resolve, reject) => {
      handleApiResponse(
        response,
        (data) => resolve(data),
        (error) => reject(new Error(error))
      );
    });
}