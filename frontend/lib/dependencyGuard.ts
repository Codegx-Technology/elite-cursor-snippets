// frontend/lib/dependencyGuard.ts

import { PlanStatus } from "@/widgets/PlanGuardWidget/types";

interface DependencyCheckResult {
  allowed: boolean;
  message: string;
  grace?: boolean;
  mode?: "slowdown" | "view_only" | "locked" | "healthy";
  planStatus?: PlanStatus; // Optional: full plan status from backend
}

/**
 * Utility to check widget dependencies against the backend PlanGuard.
 * @param userId The ID of the current user.
 * @param widgetName The name of the widget being checked.
 * @param dependencies An array of strings representing the widget's dependencies.
 * @returns A Promise resolving to a DependencyCheckResult object.
 */
export async function checkWidgetDependencies(userId: string, widgetName: string, dependencies: string[]): Promise<DependencyCheckResult> {
  try {
    const response = await fetch('/api/check-widget-dependencies', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ userId, widgetName, dependencies }),
    });

    const data = await response.json();

    if (!response.ok) {
      // Backend returned an error status (e.g., 403 Forbidden, 500 Internal Server Error)
      return {
        allowed: false,
        message: data.message || `Failed to check dependencies for ${widgetName}.`,
        mode: data.state || "locked", // Assuming backend sends state on error
        planStatus: data.planStatus, // Assuming backend sends planStatus on error
      };
    }

    // Backend returned 200 OK, but might still indicate not allowed
    return {
      allowed: data.allowed,
      message: data.message,
      grace: data.is_in_grace_mode, // Assuming backend sends this
      mode: data.state, // Assuming backend sends this
      planStatus: data.planStatus, // Assuming backend sends this
    };

  } catch (error: unknown) {
    console.error(`Error checking dependencies for widget ${widgetName}:`, error);
    const message = error instanceof Error ? error.message : String(error);
    return {
      allowed: false,
      message: `Network error or unexpected response: ${message}`,
      mode: "locked", // Default to locked on network error
    };
  }
}
