// [SNIPPET]: thinkwithai + kenyafirst + refactorclean + taskchain
// [CONTEXT]: Phase 3 - Performance optimization configuration
// [GOAL]: Advanced Next.js optimization for enterprise-grade performance
// [TASK]: Implement code splitting, image optimization, and caching strategies

/** @type {import('next').NextConfig} */
const nextConfig = {
  // Performance optimizations
  experimental: {
    optimizeCss: true,
  },

  // Image optimization with Kenya-first considerations
  images: {
    formats: ['image/webp', 'image/avif'],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
    domains: ['localhost', 'shujaa.co.ke', 'cdn.shujaa.co.ke'],
    dangerouslyAllowSVG: true
  },

  // Compression and optimization
  compress: true,
  poweredByHeader: false,
  
  // Simplified webpack configuration
  webpack: (config, { dev, webpack }) => {
    // Add performance monitoring in development only
    if (dev) {
      config.plugins.push(
        new webpack.DefinePlugin({
          'process.env.PERFORMANCE_MONITORING': JSON.stringify('true'),
        })
      );
    }

    return config;
  },

  // Headers for performance and security
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'Referrer-Policy',
            value: 'origin-when-cross-origin',
          },
          // Performance headers
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
      {
        source: '/api/(.*)',
        headers: [
          {
            key: 'Cache-Control',
            value: 'no-store, max-age=0',
          },
        ],
      },
      // Static assets caching
      {
        source: '/_next/static/(.*)',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
    ];
  },

  // Redirects for Kenya-first routing
  async redirects() {
    return [
      {
        source: '/home',
        destination: '/',
        permanent: true,
      },
      {
        source: '/dashboard/:path*',
        destination: '/dashboard/:path*',
        has: [
          {
            type: 'cookie',
            key: 'jwt_token',
          },
        ],
        permanent: false,
      },
    ];
  },

  // Environment variables for performance monitoring
  env: {
    PERFORMANCE_MONITORING: process.env.NODE_ENV === 'development' ? 'true' : 'false',
    KENYA_FIRST_MODE: 'true',
  },
};

const withNextIntl = require('next-intl/plugin')('./i18n.ts');

module.exports = withNextIntl(nextConfig);
