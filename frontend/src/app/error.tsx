'use client';

import React, { useEffect } from 'react';

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
          <svg className="w-8 h-8 text-red-600" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
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
