import { routeTask, RouteOptions } from "./routing";
import { executeWithFallback } from "./executor/provider.executor";
import { TaskType } from "./registry/registry.types";
import { ExecutePayload } from "./providers/base.adapter";
import { makeCacheKey, getCache, setCache } from "./cache/cache";

export interface OrchestrateOptions extends RouteOptions {
  // later: cache policy, timeouts, tracing IDs, etc.
}

export async function orchestrate(
  taskType: TaskType,
  payload: ExecutePayload,
  opts?: OrchestrateOptions
) {
  const plan = routeTask(taskType, { preferredModelName: opts?.preferredModelName });

  // cache-first
  const primaryModelId = plan.orderedProviders[0]?.modelId;
  const cacheKey = makeCacheKey(taskType, primaryModelId, payload);
  const cached = await getCache(cacheKey);
  if (cached) return { ok: true, data: cached, provider: "cache", modelId: primaryModelId };

  const result = await executeWithFallback(plan, payload);
  if (result.ok) {
    await setCache(cacheKey, result.data);
  }
  return result;
}
