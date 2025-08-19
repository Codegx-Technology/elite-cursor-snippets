'use client';

import React, { useEffect } from 'react';
import { FaTriangleExclamation } from 'react-icons/fa6';

// Next.js app router route-level error boundary
// This component is rendered when an error is thrown in a route segment.
export default function Error({ error, reset }: { error: Error & { digest?: string }; reset: () => void }) {
  useEffect(() => {
    // You could log to your logging infra here
    console.error('Route error:', error);
  }, [error]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center p-6">
      <div className="max-w-md w-full elite-card p-8 text-center">
        <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <FaTriangleExclamation className="text-3xl text-red-600" />
        </div>
        <h1 className="section-title mb-2">Something went wrong</h1>
        <p className="section-subtitle mb-6">An unexpected error occurred. Please try again.</p>
        <details className="text-left bg-gray-50 rounded-lg p-3 mb-6 text-xs text-red-700 whitespace-pre-wrap">
          {error?.message}
          {error?.digest ? `\nDigest: ${error.digest}` : ''}
        </details>
        <div className="flex gap-3 justify-center">
          <button className="btn-primary" onClick={() => reset()}>Try again</button>
          <button className="btn-secondary" onClick={() => window.location.assign('/')}>Go Home</button>
        </div>
      </div>
    </div>
  );
}
