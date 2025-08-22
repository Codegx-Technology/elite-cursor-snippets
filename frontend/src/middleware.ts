import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

// surgicalfix + uxfix: Force a single dev origin to avoid Next dev overlay fallback/MIME issues.
// In development, redirect 127.0.0.1 -> localhost preserving path, query, and protocol.
export function middleware(request: NextRequest) {
  // Temporarily disabled to debug _next 404s
  return NextResponse.next();
}

export const config = {
  // Disable middleware during debugging
  matcher: [],
};
