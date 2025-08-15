import { RoutedPlan } from "../routing";
import { ProviderAdapter, ExecutePayload, ExecuteResult } from "../providers/base.adapter";
import { GeminiAdapter } from "../providers";
import { ProviderIdentifier } from "../registry/registry.types";

const ADAPTERS: ProviderAdapter[] = [
  GeminiAdapter,
  // Later: HFAdapter, ReplicateAdapter, StabilityAdapter, RunPodAdapter, LocalAdapter, KaggleAdapter, ColabAdapter
];

function pickAdapter(providerName: string): ProviderAdapter | undefined {
  return ADAPTERS.find((a) => a.name === providerName);
}

export async function executeWithFallback(
  plan: RoutedPlan,
  payload: ExecutePayload
): Promise<ExecuteResult> {
  let lastError: Error | undefined;

  for (const id of plan.orderedProviders) {
    const adapter = pickAdapter(id.provider);
    if (!adapter) continue;
    if (!adapter.supports(plan.taskType)) continue;

    const res = await adapter.execute(plan.taskType, id as ProviderIdentifier, payload);
    if (res.ok) return res;
    lastError = res.error;
  }

  return { ok: false, error: lastError ?? new Error("No provider available"), provider: "n/a" };
}
