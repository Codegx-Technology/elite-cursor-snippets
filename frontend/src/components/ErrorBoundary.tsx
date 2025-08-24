'use client';

import React from 'react';
import { FaFlag, FaMountain, FaExclamationTriangle, FaRedoAlt } from 'react-icons/fa';
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
      const errorReport = {
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

  private reportError = (errorReport: any) => {
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
              <FaFlag className="text-3xl text-green-600" />
              <FaMountain className="text-3xl text-yellow-500" />
            </div>
          </div>
          <h1 className="text-2xl font-bold text-gray-800 mb-2">Shujaa Studio</h1>
          <p className="text-gray-600">Kenya-First AI Video Platform</p>
        </div>

        {/* Error Icon */}
        <div className="mb-6">
          <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <FaExclamationTriangle className="text-3xl text-red-600" />
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
            <FaRedoAlt />
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
      <FaExclamationTriangle className="text-red-600 text-2xl mx-auto mb-2" />
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
