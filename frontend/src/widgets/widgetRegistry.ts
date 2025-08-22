import React from 'react';

// Define a type for a widget entry in the registry
export interface WidgetRegistryEntry {
  component: React.ComponentType<any>;
  dependencies: string[]; // List of conceptual dependencies (e.g., "core_ai", "analytics_plus")
  description: string;
  // Add other metadata as needed (e.g., version, author, category)
}

// Centralized registry for all widgets
// In a real application, this might be dynamically loaded or generated
const widgetRegistry = new Map<string, WidgetRegistryEntry>();

// Example: Registering the PlanGuardWidget
// Lazy load the component to improve initial bundle size
widgetRegistry.set("PlanGuardWidget", {
  component: React.lazy(() => import('./PlanGuardWidget/PlanGuardWidget')), // Path relative to this file
  dependencies: ["core_ai", "realtime_updates"], // Example dependencies
  description: "Displays user plan status and grace period countdown.",
});

// Example: Registering the PlanGuardDashboardWidget
widgetRegistry.set("PlanGuardDashboardWidget", {
  component: React.lazy(() => import('./PlanGuardDashboardWidget/PlanGuardDashboardWidget')), // Path relative to this file
  dependencies: ["analytics_pro", "reporting_suite"], // Example dependencies
  description: "Provides a detailed overview of user usage and enforcement history.",
});

// Example: Registering the SuperAdminDashboard
widgetRegistry.set("SuperAdminDashboard", {
  component: React.lazy(() => import('./SuperAdminDashboard')), // Path to the new index.tsx
  dependencies: ["admin_access"], // Requires admin access
  description: "Provides a comprehensive dashboard for Super Administrators.",
});

// Example: Registering the UserPlanDashboardWidget
widgetRegistry.set("UserPlanDashboardWidget", {
  component: React.lazy(() => import('./UserPlanDashboard')), // Path to the new index.tsx
  dependencies: ["user_dashboard_access"], // Example dependency
  description: "Provides a user-facing dashboard for plan and usage tracking.",
});

// Add other widgets here as they are developed

export default widgetRegistry;
