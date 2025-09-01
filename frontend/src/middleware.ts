import createMiddleware from 'next-intl/middleware';

export default createMiddleware({
  // A list of all locales that are supported
  locales: ['en', 'sw'],

  // Used when no locale matches
  defaultLocale: 'en',

  // Don't redirect root path
  localePrefix: 'as-needed'
});

export const config = {
  // Match only internationalized pathnames, exclude working pages and main app routes
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico|minimal|test|simple|dashboard|admin|analytics|assets|audio-studio|gallery|generate|login|profile|projects|register|settings|team|users|video-generate|news-generate).*)']
};
