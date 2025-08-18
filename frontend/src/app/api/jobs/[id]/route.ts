import { NextRequest, NextResponse } from 'next/server';

// TODO: Fix Next.js API route typing bug
export async function GET(
  _request: any,
  context: any
) {
  const baseUrl = process.env.BACKEND_URL || 'http://localhost:8000'
  const target = `${baseUrl.replace(/\/$/, '')}/api/jobs/${encodeURIComponent(context.params.id)}`

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