// Simple in-memory job store for dev
// NOTE: This resets on server restart. For production, persist to DB/Redis.

export type JobStatus = 'pending' | 'processing' | 'completed' | 'failed';

export interface JobRecord {
  id: string;
  type: 'video' | 'news_video' | 'image' | 'audio';
  status: JobStatus;
  progress: number;
  created_at: string;
  completed_at?: string;
  result_url?: string;
  error_message?: string;
  metadata: Record<string, any>;
}

// Persist across Next.js dev HMR by attaching to globalThis
const g = globalThis as unknown as { __SHUJAA_JOBS__?: Map<string, JobRecord> };
if (!g.__SHUJAA_JOBS__) {
  g.__SHUJAA_JOBS__ = new Map<string, JobRecord>();
}
const jobs = g.__SHUJAA_JOBS__ as Map<string, JobRecord>;

export function createJob(partial: Partial<JobRecord> & { id: string }): JobRecord {
  const job: JobRecord = {
    id: partial.id,
    type: 'video',
    status: partial.status ?? 'pending',
    progress: partial.progress ?? 0,
    created_at: new Date().toISOString(),
    metadata: partial.metadata ?? {},
  };
  jobs.set(job.id, job);
  return job;
}

export function updateJob(id: string, updates: Partial<JobRecord>): JobRecord | null {
  const job = jobs.get(id);
  if (!job) return null;
  const next = { ...job, ...updates } as JobRecord;
  jobs.set(id, next);
  return next;
}

export function getJob(id: string): JobRecord | null {
  return jobs.get(id) ?? null;
}

export function listJobs(): JobRecord[] {
  return Array.from(jobs.values()).sort((a, b) => (a.created_at < b.created_at ? 1 : -1));
}
