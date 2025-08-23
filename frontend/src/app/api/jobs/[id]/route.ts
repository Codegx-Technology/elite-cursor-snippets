import { NextResponse } from 'next/server';

interface ErrorResponse {
  error?: string;
  detail?: string;
}

export async function GET(
  _request: Request,
  context: { params: { id: string } }
) {
  const baseUrl = process.env.BACKEND_URL || 'http://localhost:8000'
  const target = `${baseUrl.replace(/\/$/, '')}/api/jobs/${encodeURIComponent(context.params.id)}`

  try {
    const res = await fetch(target, {
      headers: { Accept: 'application/json' },
      // Ensure fresh status when polling
      cache: 'no-store',
    })

    let data: unknown = null
    try {
      data = await res.json()
    } catch {
      data = null
    }

    if (!res.ok) {
      let message = 'Job not found';
      if (data && typeof data === 'object') {
        const errorResponse = data as ErrorResponse;
        if (errorResponse.error) {
          message = errorResponse.error;
        } else if (errorResponse.detail) {
          message = errorResponse.detail;
        }
      }
      return NextResponse.json({ error: message }, { status: res.status })
    }

    return NextResponse.json(data, { status: res.status })
  } catch {
    return NextResponse.json(
      { error: 'Backend unreachable' },
      { status: 502 }
    )
  }
}