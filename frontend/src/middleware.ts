import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

// surgicalfix + uxfix: Force a single dev origin to avoid Next dev overlay fallback/MIME issues.
// In development, redirect 127.0.0.1 -> localhost preserving path, query, and protocol.
export function middleware(request: NextRequest) {
  if (process.env.NODE_ENV !== 'production') {
    const url = request.nextUrl.clone();
    const loopbackHosts = new Set(['127.0.0.1', '::1', '0.0.0.0']);
    if (loopbackHosts.has(url.hostname)) {
      url.hostname = 'localhost';
      return NextResponse.redirect(url, 307);
    }
  }
  return NextResponse.next();
}

export const config = {
  // Apply to all paths
  matcher: '/:path*',
};
