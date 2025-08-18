import { getModelRoute } from "../registry/registry.helpers";
import { ProviderIdentifier, TaskType } from "../registry/registry.types";

export interface RouteOptions {
  preferredModelName?: string;
  priority?: "cost" | "latency" | "quality"; // future use
}

export interface RoutedPlan {
  taskType: TaskType;
  orderedProviders: ProviderIdentifier[];
}

export function routeTask(
  taskType: TaskType,
  options?: RouteOptions
): RoutedPlan {
  const route = getModelRoute(taskType, {
    preferredModelName: options?.preferredModelName,
  });

  // TODO: later apply health/cost signals here to reorder route.candidateProviders
  return {
    taskType,
    orderedProviders: route.candidateProviders,
  };
}
