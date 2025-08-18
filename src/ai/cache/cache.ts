import crypto from "node:crypto";
const store = new Map<string, any>(); // swap with Redis/DB later

export function makeCacheKey(taskType: string, modelId: string | undefined, payload: unknown) {
  const h = crypto.createHash("sha256");
  h.update(taskType);
  h.update("::");
  h.update(modelId ?? "no-model");
  h.update("::");
  h.update(JSON.stringify(payload ?? {}));
  return h.digest("hex");
}

export async function getCache<T = any>(key: string): Promise<T | undefined> {
  return store.get(key);
}

export async function setCache<T = any>(key: string, value: T): Promise<void> {
  store.set(key, value);
}
