'use client';

import { FaFlag, FaMountain } from 'react-icons/fa';

// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorintent
// [CONTEXT]: Loading page component with Kenya-first design for better UX
// [GOAL]: Create beautiful loading experience that maintains cultural authenticity
// [TASK]: Implement loading component with proper animations and responsive design

interface LoadingPageProps {
  message?: string;
  showProgress?: boolean;
  progress?: number;
}

export default function LoadingPage({ 
  message = 'Loading...', 
  showProgress = false, 
  progress = 0 
}: LoadingPageProps) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center">
      <div className="text-center max-w-md mx-auto px-6">
        {/* Kenya-First Branding */}
        <div className="mb-8">
          <div className="flex items-center justify-center space-x-3 mb-4">
            <div className="flex items-center space-x-1">
              <FaFlag className="text-3xl text-green-600 animate-pulse" />
              <FaMountain className="text-3xl text-yellow-500 animate-float" />
            </div>
          </div>
          <h1 className="text-2xl font-bold text-gray-800 mb-2">Shujaa Studio</h1>
          <p className="text-gray-600">Kenya-First AI Video Platform</p>
        </div>

        {/* Loading Animation */}
        <div className="mb-6">
          <div className="relative">
            <div className="w-16 h-16 border-4 border-green-200 border-t-green-600 rounded-full animate-spin mx-auto mb-4"></div>
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="w-6 h-6 border-2 border-green-600 border-t-transparent rounded-full animate-spin"></div>
            </div>
          </div>
        </div>

        {/* Loading Message */}
        <div className="mb-6">
          <p className="text-gray-700 font-medium mb-2">{message}</p>
          {showProgress && (
            <div className="w-full bg-gray-200 rounded-full h-2 mb-2">
              <div 
                className="bg-gradient-to-r from-green-600 to-blue-600 h-2 rounded-full transition-all duration-300 ease-out"
                style={{ width: `${Math.min(100, Math.max(0, progress))}%` }}
              ></div>
            </div>
          )}
          {showProgress && (
            <p className="text-sm text-gray-500">{Math.round(progress)}% complete</p>
          )}
        </div>

        {/* Cultural Footer */}
        <div className="bg-gradient-to-r from-green-600 via-red-600 to-black p-4 rounded-lg text-white text-center">
          <p className="text-sm">
            🇰🇪 Proudly Kenyan • Harambee Spirit • Innovation for Africa
          </p>
        </div>
      </div>
    </div>
  );
}

// Skeleton loading component for individual sections
export function SkeletonLoader({ className = '' }: { className?: string }) {
  return (
    <div className={`animate-pulse ${className}`}>
      <div className="bg-gray-200 rounded-lg h-4 mb-2"></div>
      <div className="bg-gray-200 rounded-lg h-4 w-3/4 mb-2"></div>
      <div className="bg-gray-200 rounded-lg h-4 w-1/2"></div>
    </div>
  );
}

// Card skeleton for dashboard
export function CardSkeleton() {
  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6 animate-pulse">
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <div className="bg-gray-200 rounded h-4 w-24 mb-2"></div>
          <div className="bg-gray-200 rounded h-8 w-16"></div>
        </div>
        <div className="bg-gray-200 rounded-full w-12 h-12"></div>
      </div>
    </div>
  );
}

// List item skeleton
export function ListItemSkeleton() {
  return (
    <div className="flex items-center space-x-4 p-4 bg-gray-50 rounded-lg animate-pulse">
      <div className="bg-gray-200 rounded-full w-12 h-12"></div>
      <div className="flex-1">
        <div className="bg-gray-200 rounded h-4 w-3/4 mb-2"></div>
        <div className="bg-gray-200 rounded h-3 w-1/2"></div>
      </div>
      <div className="bg-gray-200 rounded h-6 w-16"></div>
    </div>
  );
}

