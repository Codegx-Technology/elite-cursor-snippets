type Health = { up: boolean; avgLatencyMs: number; samples: number };
const STATE = new Map<string, Health>();

export async function pingProvider(name: string, fn: () => Promise<void>) {
  const start = Date.now();
  try {
    await fn();
    const ms = Date.now() - start;
    const prev = STATE.get(name) ?? { up: true, avgLatencyMs: ms, samples: 0 };
    const samples = prev.samples + 1;
    const avgLatencyMs = (prev.avgLatencyMs * prev.samples + ms) / samples;
    STATE.set(name, { up: true, avgLatencyMs, samples });
  } catch {
    const prev = STATE.get(name) ?? { up: false, avgLatencyMs: 9999, samples: 0 };
    STATE.set(name, { ...prev, up: false });
  }
}

export function getHealth(name: string): Health {
  return STATE.get(name) ?? { up: true, avgLatencyMs: 0, samples: 0 };
}
