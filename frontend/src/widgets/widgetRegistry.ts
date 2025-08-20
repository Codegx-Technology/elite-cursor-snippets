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
  component: React.lazy(() => import('./PlanGuardWidget')), // Path relative to this file
  dependencies: ["core_ai", "realtime_updates"], // Example dependencies
  description: "Displays user plan status and grace period countdown.",
});

// Example: Registering the PlanGuardDashboardWidget
widgetRegistry.set("PlanGuardDashboardWidget", {
  component: React.lazy(() => import('./PlanGuardDashboardWidget')), // Path relative to this file
  dependencies: ["analytics_pro", "reporting_suite"], // Example dependencies
  description: "Provides a detailed overview of user usage and enforcement history.",
});

// Add other widgets here as they are developed

export default widgetRegistry;
