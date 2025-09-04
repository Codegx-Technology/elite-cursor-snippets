'use client';

import React from 'react';
import { perfMonitor } from '@/lib/performance';
import { useAriaUtils } from '@/hooks/useAccessibility';

// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorintent
// [CONTEXT]: Error boundary component with Kenya-first design for production readiness
// [GOAL]: Create robust error handling with cultural authenticity and user-friendly recovery
// [TASK]: Implement error boundary with proper error reporting and recovery options

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
  errorInfo: React.ErrorInfo | null;
}

interface ErrorBoundaryProps {
  children: React.ReactNode;
  fallback?: React.ComponentType<{ error: Error; retry: () => void }>;
}

interface ErrorReport {
  message: string;
  stack?: string;
  componentStack?: string;
  timestamp: string;
  userAgent: string;
  url: string;
  kenyaFirstContext: string;
}

class ErrorBoundary extends React.Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null,
    };
  }

  static getDerivedStateFromError(error: Error): Partial<ErrorBoundaryState> {
    return {
      hasError: true,
      error,
    };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    this.setState({
      error,
      errorInfo,
    });

    // Performance monitoring for errors
    perfMonitor.startTiming('error_recovery');
    
    // Log error with Kenya-first context
    console.error('🇰🇪 Error caught by boundary:', error, errorInfo);
    
    // Enhanced error reporting for production
    if (process.env.NODE_ENV === 'production') {
      const errorReport: ErrorReport = {
        message: error.message,
        stack: error.stack,
        componentStack: errorInfo.componentStack,
        timestamp: new Date().toISOString(),
        userAgent: navigator.userAgent,
        url: window.location.href,
        kenyaFirstContext: 'Enterprise SaaS Platform'
      };
      
      // Send to monitoring service (implement your preferred service)
      this.reportError(errorReport);
    }
  }

  private reportError = (errorReport: ErrorReport) => {
    // Implement error reporting to your monitoring service
    // e.g., Sentry, LogRocket, custom endpoint
    fetch('/api/errors', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(errorReport)
    }).catch(() => {
      // Fallback: store in localStorage for later retry
      const errors = JSON.parse(localStorage.getItem('pending_errors') || '[]');
      errors.push(errorReport);
      localStorage.setItem('pending_errors', JSON.stringify(errors));
    });
  };

  handleRetry = () => {
    perfMonitor.endTiming('error_recovery');
    this.setState({
      hasError: false,
      error: null,
      errorInfo: null,
    });
  };

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        const FallbackComponent = this.props.fallback;
        return <FallbackComponent error={this.state.error!} retry={this.handleRetry} />;
      }

      return <DefaultErrorFallback error={this.state.error!} retry={this.handleRetry} />;
    }

    return this.props.children;
  }
}

// Default error fallback component
function DefaultErrorFallback({ error, retry }: { error: Error; retry: () => void }) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center">
      <div className="text-center max-w-md mx-auto px-6">
        {/* Kenya-First Branding */}
        <div className="mb-8">
          <div className="flex items-center justify-center space-x-3 mb-4">
            <div className="flex items-center space-x-1">
              <svg className="w-8 h-8 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                <path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z" />
              </svg>
              <svg className="w-8 h-8 text-yellow-500" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" />
              </svg>
            </div>
          </div>
          <h1 className="text-2xl font-bold text-gray-800 mb-2">Shujaa Studio</h1>
          <p className="text-gray-600">Kenya-First AI Video Platform</p>
        </div>

        {/* Error Icon */}
        <div className="mb-6">
          <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg className="w-8 h-8 text-red-600" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
          </div>
        </div>

        {/* Error Message */}
        <div className="mb-8">
          <h2 className="text-xl font-bold text-gray-800 mb-4">Oops! Something went wrong</h2>
          <p className="text-gray-600 mb-4">
            We encountered an unexpected error. Don&apos;t worry, our team has been notified and we&apos;re working to fix it.
          </p>
          
          {process.env.NODE_ENV === 'development' && (
            <details className="text-left bg-gray-100 rounded-lg p-4 mb-4">
              <summary className="cursor-pointer font-medium text-gray-700 mb-2">
                Error Details (Development)
              </summary>
              <pre className="text-xs text-red-600 overflow-auto">
                {error.message}
                {error.stack}
              </pre>
            </details>
          )}
        </div>

        {/* Action Buttons */}
        <div className="space-y-4 mb-8">
          <button
            onClick={retry}
            className="w-full bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg font-medium transition-colors duration-200 flex items-center justify-center space-x-2"
          >
            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clipRule="evenodd" />
            </svg>
            <span>Try Again</span>
          </button>
          
          <button
            onClick={() => window.location.href = '/dashboard'}
            className="w-full bg-gray-600 hover:bg-gray-700 text-white px-6 py-3 rounded-lg font-medium transition-colors duration-200"
          >
            Go to Dashboard
          </button>
          
          <button
            onClick={() => window.location.reload()}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium transition-colors duration-200"
          >
            Reload Page
          </button>
        </div>

        {/* Cultural Footer */}
        <div className="bg-gradient-to-r from-green-600 via-red-600 to-black p-4 rounded-lg text-white text-center">
          <p className="text-sm">
            🇰🇪 Asante for your patience • We&apos;ll be back stronger • Harambee!
          </p>
        </div>
      </div>
    </div>
  );
}

// Hook for functional components to handle errors
export function useErrorHandler() {
  return (error: Error, errorInfo?: React.ErrorInfo) => {
    console.error('Error caught by hook:', error, errorInfo);
    
    // In production, send to error monitoring service
    if (process.env.NODE_ENV === 'production') {
      // Send to monitoring service
    }
  };
}

// Simple error fallback for smaller components
export function SimpleErrorFallback({ 
  error, 
  retry, 
  message = 'Something went wrong' 
}: { 
  error: Error; 
  retry: () => void; 
  message?: string;
}) {
  return (
    <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-center">
      <svg className="w-6 h-6 text-red-600 mx-auto mb-2" fill="currentColor" viewBox="0 0 20 20">
        <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
      </svg>
      <p className="text-red-800 font-medium mb-2">{message}</p>
      <button
        onClick={retry}
        className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg text-sm transition-colors duration-200"
      >
        Try Again
      </button>
    </div>
  );
}

export default ErrorBoundary;
