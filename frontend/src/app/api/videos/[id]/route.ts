import { NextResponse } from 'next/server'
import fs from 'fs'
import path from 'path'

// Streams the generated mp4 from project /output folder by job id (timestamp)
export async function GET(_request: Request, { params }: { params: { id: string } }) {
  const jobId = params.id
  try {
    const projectRoot = path.resolve(process.cwd(), '..')
    const out1 = path.join(projectRoot, 'output', `kenya_patriotic_60s_${jobId}_audio.mp4`)
    const out2 = path.join(projectRoot, 'output', `kenya_patriotic_60s_${jobId}.mp4`)
    const filePath = fs.existsSync(out1) ? out1 : fs.existsSync(out2) ? out2 : null

    if (!filePath) {
      return NextResponse.json({ error: 'Video not found' }, { status: 404 })
    }

    const stat = fs.statSync(filePath)
    const file = fs.createReadStream(filePath)

    return new NextResponse(file as any, {
      status: 200,
      headers: new Headers({
        'Content-Type': 'video/mp4',
        'Content-Length': stat.size.toString(),
        'Content-Disposition': `inline; filename=${path.basename(filePath)}`,
      }),
    })
  } catch (e: any) {
    return NextResponse.json({ error: e?.message || 'Failed to read video' }, { status: 500 })
  }
}
