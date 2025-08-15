import { NextResponse } from 'next/server'
// [SNIPPET]: surgicalfix + refactorclean (elite-cursor-snippets)
// [TASK]: Align Next route with FastAPI backend contract and status codes
// [GOAL]: Proxy to backend /api/jobs/{id}, pass-through status, normalize error shapes

export async function GET(_request: Request, { params }: { params: { id: string } }) {
  const baseUrl = process.env.BACKEND_URL || 'http://localhost:8000'
  const target = `${baseUrl.replace(/\/$/, '')}/api/jobs/${encodeURIComponent(params.id)}`

  try {
    const res = await fetch(target, {
      headers: { Accept: 'application/json' },
      // Ensure fresh status when polling
      cache: 'no-store',
    })

    let data: any = null
    try {
      data = await res.json()
    } catch {
      data = null
    }

    if (!res.ok) {
      const message = (data && (data.error || data.detail)) || 'Job not found'
      return NextResponse.json({ error: message }, { status: res.status })
    }

    return NextResponse.json(data, { status: res.status })
  } catch (err) {
    return NextResponse.json(
      { error: 'Backend unreachable' },
      { status: 502 }
    )
  }
}
