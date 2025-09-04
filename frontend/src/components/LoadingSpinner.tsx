'use client';

import React from 'react';
import { FaFlag, FaMountain, FaSpinner } from 'react-icons/fa6';

// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorclean
// [CONTEXT]: Enterprise-grade loading spinner with Kenya-first design
// [GOAL]: Create beautiful, culturally authentic loading animations
// [TASK]: Implement loading spinner with Kenya flag colors and cultural elements

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg' | 'xl';
  variant?: 'default' | 'kenya' | 'cultural' | 'minimal';
  text?: string;
  className?: string;
}

export default function LoadingSpinner({ 
  size = 'md', 
  variant = 'default',
  text,
  className = ''
}: LoadingSpinnerProps) {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12',
    xl: 'w-16 h-16'
  };

  const textSizeClasses = {
    sm: 'text-sm',
    md: 'text-base',
    lg: 'text-lg',
    xl: 'text-xl'
  };

  if (variant === 'kenya') {
    return (
      <div className={`flex flex-col items-center justify-center space-y-4 ${className}`}>
        <div className="relative">
          {/* Outer ring - Kenya Green */}
          <div className={`${sizeClasses[size]} border-4 border-transparent border-t-green-600 rounded-full animate-spin`}></div>
          
          {/* Inner ring - Kenya Red */}
          <div className={`absolute top-1 left-1 ${
            size === 'sm' ? 'w-2 h-2' :
            size === 'md' ? 'w-4 h-4' :
            size === 'lg' ? 'w-8 h-8' : 'w-12 h-12'
          } border-2 border-transparent border-t-red-500 rounded-full animate-spin`} 
          style={{ animationDirection: 'reverse', animationDuration: '0.8s' }}></div>
          
          {/* Center icon */}
          <div className="absolute inset-0 flex items-center justify-center">
            <FaFlag className={`${
              size === 'sm' ? 'text-xs' :
              size === 'md' ? 'text-sm' :
              size === 'lg' ? 'text-base' : 'text-lg'
            } text-yellow-500 animate-pulse`} />
          </div>
        </div>
        
        {text && (
          <div className={`${textSizeClasses[size]} font-medium text-gray-700 animate-pulse`}>
            {text}
          </div>
        )}
      </div>
    );
  }

  if (variant === 'cultural') {
    return (
      <div className={`flex flex-col items-center justify-center space-y-4 ${className}`}>
        <div className="relative">
          {/* Mountain-inspired loading */}
          <div className={`${sizeClasses[size]} relative`}>
            <div className="absolute inset-0 rounded-full bg-gradient-to-r from-yellow-400 via-red-500 to-green-600 animate-spin"></div>
            <div className="absolute inset-1 rounded-full bg-white flex items-center justify-center">
              <FaMountain className={`${
                size === 'sm' ? 'text-xs' :
                size === 'md' ? 'text-sm' :
                size === 'lg' ? 'text-base' : 'text-lg'
              } text-gray-600 animate-pulse`} />
            </div>
          </div>
        </div>
        
        {text && (
          <div className={`${textSizeClasses[size]} font-medium text-gradient-cultural animate-pulse`}>
            {text}
          </div>
        )}
      </div>
    );
  }

  if (variant === 'minimal') {
    return (
      <div className={`flex items-center justify-center space-x-2 ${className}`}>
        <div className={`${sizeClasses[size]} border-2 border-gray-300 border-t-blue-600 rounded-full animate-spin`}></div>
        {text && (
          <span className={`${textSizeClasses[size]} text-gray-600`}>
            {text}
          </span>
        )}
      </div>
    );
  }

  // Default variant
  return (
    <div className={`flex flex-col items-center justify-center space-y-3 ${className}`}>
      <div className="relative">
        <div className={`${sizeClasses[size]} border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin`}></div>
      </div>
      
      {text && (
        <div className={`${textSizeClasses[size]} font-medium text-gray-700`}>
          {text}
        </div>
      )}
    </div>
  );
}

// Preset loading components for common use cases
export const KenyaLoader = ({ text = "Loading..." }: { text?: string }) => (
  <LoadingSpinner variant="kenya" size="lg" text={text} />
);

export const CulturalLoader = ({ text = "Preparing your content..." }: { text?: string }) => (
  <LoadingSpinner variant="cultural" size="lg" text={text} />
);

export const MinimalLoader = ({ text }: { text?: string }) => (
  <LoadingSpinner variant="minimal" size="md" text={text} />
);

// Full-screen loading overlay
export const LoadingOverlay = ({ 
  isVisible, 
  text = "Loading...", 
  variant = 'kenya' 
}: { 
  isVisible: boolean; 
  text?: string; 
  variant?: 'default' | 'kenya' | 'cultural' | 'minimal';
}) => {
  if (!isVisible) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 backdrop-blur-sm">
      <div className="bg-white rounded-2xl p-8 shadow-2xl">
        <LoadingSpinner variant={variant} size="xl" text={text} />
      </div>
    </div>
  );
};

