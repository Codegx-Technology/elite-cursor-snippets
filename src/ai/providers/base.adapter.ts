import { ProviderIdentifier, TaskType } from "../registry/registry.types";

export interface ExecutePayload {
  prompt?: string;
  input?: unknown;
  // attach any per-task structured inputs
}

export interface ExecuteResult {
  ok: boolean;
  data?: unknown;
  error?: Error;
  provider: string;
  modelId?: string;
}

export interface ProviderAdapter {
  name: string;
  supports(task: TaskType): boolean;
  execute(task: TaskType, id: ProviderIdentifier, payload: ExecutePayload): Promise<ExecuteResult>;
}
