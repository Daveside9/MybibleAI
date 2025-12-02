import { NextResponse, type NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  // Since we are using localStorage, the middleware (which runs server-side)
  // cannot access the token. Route protection will be handled client-side.
  return NextResponse.next()
}

// Optionally, you can specify which paths the middleware should run on.
// Running it on all paths is fine for this simplified version.
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
}