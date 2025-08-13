import { NextResponse } from 'next/server'
import { spawn } from 'child_process'
import path from 'path'
import { createJob, updateJob } from '@/lib/jobStore'

export async function POST(request: Request) {
  try {
    const body = await request.json().catch(() => ({}))
    const ts = new Date().toISOString().replace(/[-:TZ.]/g, '').slice(0, 14)
    const jobId = ts // use timestamp as id for compatibility with python --ts

    // Create job
    createJob({
      id: jobId,
      status: 'processing',
      progress: 5,
      metadata: {
        request: body,
        started_by: 'react_ui',
      },
    })

    // Resolve python script path (project root is one level up from frontend)
    const projectRoot = path.resolve(process.cwd(), '..')
    const scriptPath = path.join(projectRoot, 'api_video_generator.py')

    // Spawn python process in background
    const env: NodeJS.ProcessEnv = { ...process.env, SHUJAA_TS: jobId }
    const hf = process.env.HF_API_KEY || process.env.HF_TOKEN
    if (hf) {
      env.HF_API_KEY = hf
      env.HF_TOKEN = hf
    }

    const child = spawn('python', [scriptPath, '--ts', jobId], {
      cwd: projectRoot,
      env,
      windowsHide: true,
      detached: false,
      stdio: ['ignore', 'pipe', 'pipe'],
    })

    child.stdout.on('data', (buf: Buffer) => {
      const line = buf.toString()
      // Heuristic progress updates based on log markers
      if (line.includes('requesting image')) updateJob(jobId, { progress: 20 })
      if (line.includes('Requesting TTS')) updateJob(jobId, { progress: 60 })
      if (line.includes('Video saved')) updateJob(jobId, { progress: 90 })
      const m = line.match(/SUCCESS: Video created: (.*)/)
      if (m) {
        updateJob(jobId, {
          status: 'completed',
          progress: 100,
          completed_at: new Date().toISOString(),
          // Serve via Next route to avoid exposing filesystem paths
          result_url: `/api/videos/${jobId}`,
        })
      }
    })

    child.stderr.on('data', (buf: Buffer) => {
      // Surface errors but keep process running
      // Optionally could aggregate
    })

    child.on('error', (err) => {
      updateJob(jobId, {
        status: 'failed',
        progress: 0,
        error_message: `Spawn error: ${err.message}`,
        completed_at: new Date().toISOString(),
      })
    })

    child.on('close', (code) => {
      if (code !== 0) {
        updateJob(jobId, {
          status: 'failed',
          progress: 0,
          error_message: `Process exited with code ${code}`,
          completed_at: new Date().toISOString(),
        })
      }
    })

    return NextResponse.json(
      {
        status: 'queued',
        video_id: jobId,
        message: 'Generation started',
        progress: 5,
      },
      { status: 202 }
    )
  } catch (e: any) {
    return NextResponse.json(
      { error: e?.message || 'Failed to start generation', status: 'error' },
      { status: 500 }
    )
  }
}
