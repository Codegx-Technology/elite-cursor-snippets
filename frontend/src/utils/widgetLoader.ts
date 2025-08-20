import React, { useState, useEffect } from 'react';
import widgetRegistry from '@/widgets/widgetRegistry';
import { usePlanGuard } from '@/context/PlanGuardContext'; // New import
import type { PlanStatus } from '@/widgets/PlanGuardWidget/types';

interface WidgetLoadResult {
  component: React.ComponentType<any> | null;
  allowed: boolean;
  message: string;
  planStatus: PlanStatus | null;
}

// This function simulates checking widget dependencies against the user's plan
// In a real scenario, this would call the backend /api/check-widget-dependencies
async function checkWidgetDependencies(userId: string | undefined, widgetName: string, currentPlanStatus: PlanStatus | null): Promise<{ allowed: boolean; message: string; planStatus: PlanStatus | null }> {
  const widgetEntry = widgetRegistry.get(widgetName);
  if (!widgetEntry) {
    return { allowed: false, message: `Widget '${widgetName}' not found in registry.`, planStatus: null };
  }

  // If plan status is not yet loaded, or there's an error, we can't check dependencies
  if (!currentPlanStatus) {
    return { allowed: false, message: "Plan status not available to check dependencies.", planStatus: null };
  }

  // Check plan state first
  if (currentPlanStatus.state === "view_only" || currentPlanStatus.state === "locked") {
    return {
      allowed: false,
      message: `Your plan is in "${currentPlanStatus.state}" mode. Please upgrade to access this feature.`,
      planStatus: currentPlanStatus,
    };
  }

  try {
    const response = await fetch('/api/check-widget-dependencies', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ dependencies: widgetEntry.dependencies, userId: userId }),
    });

    const data = await response.json();

    if (!data.allowed) {
      return { allowed: false, message: data.message, planStatus: data };
    }

    return { allowed: true, message: "", planStatus: currentPlanStatus };

  } catch (error: any) {
    console.error("Error checking widget dependencies:", error);
    return { allowed: false, message: `Failed to check widget dependencies: ${error.message || error}`, planStatus: null };
  }
}

// Custom hook to load a widget and check its permissions
export function useWidgetLoader(widgetName: string, userId?: string) {
  const [result, setResult] = useState<WidgetLoadResult>({
    component: null,
    allowed: false,
    message: "Loading...",
    planStatus: null,
  });

  const { planStatus: globalPlanStatus, loading: globalPlanLoading, error: globalPlanError } = usePlanGuard();

  useEffect(() => {
    let isMounted = true;

    async function loadWidget() {
      if (globalPlanLoading) {
        setResult(prev => ({ ...prev, message: "Loading plan status..." }));
        return;
      }
      if (globalPlanError) {
        setResult(prev => ({ ...prev, message: `Error loading plan: ${globalPlanError}` }));
        return;
      }

      const checkResult = await checkWidgetDependencies(userId, widgetName, globalPlanStatus);
      if (!isMounted) return;

      if (checkResult.allowed) {
        try {
          const widgetEntry = widgetRegistry.get(widgetName);
          if (widgetEntry) {
            const module = await widgetEntry.component();
            if (isMounted) {
              setResult({
                component: module.default,
                allowed: true,
                message: "",
                planStatus: checkResult.planStatus,
              });
            }
          } else {
            setResult({
              component: null,
              allowed: false,
              message: `Widget '${widgetName}' not found in registry.`, 
              planStatus: null,
            });
          }
        } catch (error: any) {
          console.error(`Failed to load widget '${widgetName}':`, error);
          setResult({
            component: null,
            allowed: false,
            message: `Failed to load widget '${widgetName}': ${error.message || error}`, 
            planStatus: null,
          });
        }
      } else {
        setResult({
          component: null,
          allowed: false,
          message: checkResult.message,
          planStatus: checkResult.planStatus,
        });
      }
    }

    loadWidget();

    return () => {
      isMounted = false;
    };
  }, [widgetName, userId, globalPlanStatus, globalPlanLoading, globalPlanError]);

  return result;
}
