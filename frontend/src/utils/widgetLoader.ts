import React, { useState, useEffect } from 'react';
import widgetRegistry from '@/widgets/widgetRegistry';
import { usePlanGuard } from '@/context/PlanGuardContext'; // New import
import type { PlanStatus } from '@/widgets/PlanGuardWidget/types';
import { checkWidgetDependencies as checkDependenciesFromGuard } from '@/lib/dependencyGuard'; // Import from new utility
import { getDenyMessage } from '@/ui/planMessages'; // New import

interface WidgetLoadResult {
  component: React.ComponentType<any> | null;
  allowed: boolean;
  message: string;
  planStatus: PlanStatus | null;
}

// This function now uses the centralized dependencyGuard utility
async function checkWidgetDependencies(userId: string | undefined, widgetName: string, currentPlanStatus: PlanStatus | null): Promise<{ allowed: boolean; message: string; planStatus: PlanStatus | null }> {
  const widgetEntry = widgetRegistry.get(widgetName);
  if (!widgetEntry) {
    return { allowed: false, message: `Widget '${widgetName}' not found in registry.`, planStatus: null };
  }

  // Use the imported checkDependenciesFromGuard
  const result = await checkDependenciesFromGuard(widgetName, widgetEntry.dependencies);

  // Map the result from dependencyGuard to the expected WidgetLoadResult format
  return {
    allowed: result.ok,
    message: result.reason || '',
    planStatus: currentPlanStatus,
  };
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
            if (isMounted) {
              setResult({
                component: widgetEntry.component,
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
          message: getDenyMessage(checkResult.message), // Use getDenyMessage
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
