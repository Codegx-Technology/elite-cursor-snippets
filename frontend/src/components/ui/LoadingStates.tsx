// [SNIPPET]: thinkwithai + kenyafirst + refactorclean + taskchain
// [CONTEXT]: Enterprise-grade loading states with Kenya-first design system integration
// [GOAL]: Comprehensive loading UI components with cultural authenticity
// [TASK]: Phase 2.3 - Error & Loading States with comprehensive state management UI

'use client';

import React from 'react';
import { colors, spacing, typography } from '@/config/designTokens';
import { cn } from '@/lib/utils';
import { FaSpinner, FaVideo, FaUpload, FaCog } from 'react-icons/fa6';

// Loading Spinner Component
export interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg' | 'xl';
  variant?: 'default' | 'kenya' | 'cultural' | 'elite';
  className?: string;
}

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  size = 'md',
  variant = 'default',
  className
}) => {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-6 h-6',
    lg: 'w-8 h-8',
    xl: 'w-12 h-12'
  };

  const variantClasses = {
    default: 'text-blue-600',
    kenya: `text-[${colors.kenya.green}]`,
    cultural: `text-[${colors.cultural.gold}]`,
    elite: 'text-purple-600'
  };

  return (
    <FaSpinner
      className={cn(
        'animate-spin',
        sizeClasses[size],
        variantClasses[variant],
        className
      )}
    />
  );
};

// Loading Card Component
export interface LoadingCardProps {
  title?: string;
  subtitle?: string;
  variant?: 'default' | 'kenya' | 'cultural' | 'elite';
  className?: string;
  showProgress?: boolean;
  progress?: number;
}

export const LoadingCard: React.FC<LoadingCardProps> = ({
  title = 'Inapakia...',
  subtitle = 'Tafadhali subiri',
  variant = 'default',
  className,
  showProgress = false,
  progress = 0
}) => {
  const variantClasses = {
    default: 'border-gray-200 bg-white',
    kenya: `border-[${colors.kenya.green}] border-opacity-20 bg-green-50`,
    cultural: `border-[${colors.cultural.gold}] border-opacity-30 bg-yellow-50`,
    elite: 'border-purple-200 bg-purple-50'
  };

  const progressColors = {
    default: 'bg-blue-500',
    kenya: `bg-[${colors.kenya.green}]`,
    cultural: `bg-[${colors.cultural.gold}]`,
    elite: 'bg-purple-500'
  };

  return (
    <div className={cn(
      'rounded-lg border p-6 text-center',
      variantClasses[variant],
      className
    )}>
      <div className="flex justify-center mb-4">
        <LoadingSpinner size="lg" variant={variant} />
      </div>
      
      <h3 className={cn(
        'font-semibold text-gray-900 mb-2',
        `text-[${typography.fontSizes.lg}]`
      )}>
        {title}
      </h3>
      
      <p className={cn(
        'text-gray-600 mb-4',
        `text-[${typography.fontSizes.sm}]`
      )}>
        {subtitle}
      </p>

      {showProgress && (
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className={cn('h-2 rounded-full transition-all duration-300', progressColors[variant])}
            style={{ width: `${Math.min(100, Math.max(0, progress))}%` }}
          />
        </div>
      )}
    </div>
  );
};

// Video Processing Loading
export interface VideoLoadingProps {
  stage?: 'uploading' | 'processing' | 'generating' | 'finalizing';
  variant?: 'default' | 'kenya' | 'cultural' | 'elite';
  progress?: number;
  className?: string;
}

export const VideoLoading: React.FC<VideoLoadingProps> = ({
  stage = 'processing',
  variant = 'kenya',
  progress = 0,
  className
}) => {
  const stageInfo = {
    uploading: {
      title: 'Inapakia Faili...',
      subtitle: 'Tunapakia video yako kwenye seva',
      icon: <FaUpload className="w-8 h-8" />
    },
    processing: {
      title: 'Inachakata Video...',
      subtitle: 'Tunachakata na kuhariri video yako',
      icon: <FaCog className="w-8 h-8 animate-spin" />
    },
    generating: {
      title: 'Inaunda Video...',
      subtitle: 'Tunaunda video yako ya mwisho',
      icon: <FaVideo className="w-8 h-8" />
    },
    finalizing: {
      title: 'Inamaliza...',
      subtitle: 'Tunamaliza na kuandaa video yako',
      icon: <FaSpinner className="w-8 h-8 animate-spin" />
    }
  };

  const current = stageInfo[stage];
  
  const variantClasses = {
    default: 'border-gray-200 bg-white',
    kenya: `border-[${colors.kenya.green}] border-opacity-20 bg-green-50`,
    cultural: `border-[${colors.cultural.gold}] border-opacity-30 bg-yellow-50`,
    elite: 'border-purple-200 bg-purple-50'
  };

  const iconColors = {
    default: 'text-blue-600',
    kenya: `text-[${colors.kenya.green}]`,
    cultural: `text-[${colors.cultural.gold}]`,
    elite: 'text-purple-600'
  };

  const progressColors = {
    default: 'bg-blue-500',
    kenya: `bg-[${colors.kenya.green}]`,
    cultural: `bg-[${colors.cultural.gold}]`,
    elite: 'bg-purple-500'
  };

  return (
    <div className={cn(
      'max-w-md mx-auto rounded-lg border p-8 text-center',
      variantClasses[variant],
      className
    )}>
      <div className={cn('flex justify-center mb-6', iconColors[variant])}>
        {current.icon}
      </div>
      
      <h2 className={cn(
        'font-bold text-gray-900 mb-2',
        `text-[${typography.fontSizes.xl}]`
      )}>
        {current.title}
      </h2>
      
      <p className={cn(
        'text-gray-600 mb-6',
        `text-[${typography.fontSizes.base}]`
      )}>
        {current.subtitle}
      </p>

      <div className="w-full bg-gray-200 rounded-full h-3 mb-4">
        <div
          className={cn('h-3 rounded-full transition-all duration-500', progressColors[variant])}
          style={{ width: `${Math.min(100, Math.max(0, progress))}%` }}
        />
      </div>
      
      <p className={cn(
        'text-gray-500',
        `text-[${typography.fontSizes.sm}]`
      )}>
        {progress}% Imekamilika
      </p>

      <div className="mt-6 text-xs text-gray-400">
        <p>Mchakato huu unaweza kuchukua dakika 2-5</p>
      </div>
    </div>
  );
};

// Skeleton Loading Components
export interface SkeletonProps {
  className?: string;
  variant?: 'default' | 'kenya' | 'cultural' | 'elite';
}

export const Skeleton: React.FC<SkeletonProps> = ({ className, variant = 'default' }) => {
  const variantClasses = {
    default: 'bg-gray-200',
    kenya: 'bg-green-100',
    cultural: 'bg-yellow-100',
    elite: 'bg-purple-100'
  };

  return (
    <div className={cn(
      'animate-pulse rounded',
      variantClasses[variant],
      className
    )} />
  );
};

export const SkeletonCard: React.FC<SkeletonProps> = ({ className, variant = 'default' }) => (
  <div className={cn('p-6 border rounded-lg', className)}>
    <div className="space-y-4">
      <Skeleton variant={variant} className="h-4 w-3/4" />
      <Skeleton variant={variant} className="h-4 w-1/2" />
      <Skeleton variant={variant} className="h-32 w-full" />
      <div className="flex space-x-2">
        <Skeleton variant={variant} className="h-8 w-20" />
        <Skeleton variant={variant} className="h-8 w-16" />
      </div>
    </div>
  </div>
);

export const SkeletonTable: React.FC<SkeletonProps & { rows?: number }> = ({ 
  className, 
  variant = 'default',
  rows = 5 
}) => (
  <div className={cn('border rounded-lg overflow-hidden', className)}>
    {/* Header */}
    <div className="p-4 border-b bg-gray-50 flex space-x-4">
      <Skeleton variant={variant} className="h-4 w-24" />
      <Skeleton variant={variant} className="h-4 w-32" />
      <Skeleton variant={variant} className="h-4 w-20" />
      <Skeleton variant={variant} className="h-4 w-16" />
    </div>
    
    {/* Rows */}
    {Array.from({ length: rows }).map((_, i) => (
      <div key={i} className="p-4 border-b flex space-x-4">
        <Skeleton variant={variant} className="h-4 w-24" />
        <Skeleton variant={variant} className="h-4 w-32" />
        <Skeleton variant={variant} className="h-4 w-20" />
        <Skeleton variant={variant} className="h-4 w-16" />
      </div>
    ))}
  </div>
);

// Page Loading Component
export interface PageLoadingProps {
  variant?: 'default' | 'kenya' | 'cultural' | 'elite';
  message?: string;
  showLogo?: boolean;
}

export const PageLoading: React.FC<PageLoadingProps> = ({
  variant = 'kenya',
  message = 'Inapakia ukurasa...',
  showLogo = true
}) => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="text-center">
        {showLogo && (
          <div className="mb-8">
            <div className={cn(
              'w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4',
              variant === 'kenya' ? 'bg-green-100' :
              variant === 'cultural' ? 'bg-yellow-100' :
              variant === 'elite' ? 'bg-purple-100' :
              'bg-blue-100'
            )}>
              <span className={cn(
                'text-2xl font-bold',
                variant === 'kenya' ? `text-[${colors.kenya.green}]` :
                variant === 'cultural' ? `text-[${colors.cultural.gold}]` :
                variant === 'elite' ? 'text-purple-600' :
                'text-blue-600'
              )}>
                S
              </span>
            </div>
            <h1 className="text-2xl font-bold text-gray-900 mb-2">Shujaa Studio</h1>
          </div>
        )}
        
        <LoadingSpinner size="lg" variant={variant} />
        
        <p className={cn(
          'mt-4 text-gray-600',
          `text-[${typography.fontSizes.base}]`
        )}>
          {message}
        </p>
      </div>
    </div>
  );
};

// Button Loading State
export interface LoadingButtonProps {
  children: React.ReactNode;
  loading?: boolean;
  variant?: 'default' | 'kenya' | 'cultural' | 'elite';
  size?: 'sm' | 'md' | 'lg';
  className?: string;
  disabled?: boolean;
  onClick?: () => void;
}

export const LoadingButton: React.FC<LoadingButtonProps> = ({
  children,
  loading = false,
  variant = 'default',
  size = 'md',
  className,
  disabled,
  onClick
}) => {
  const sizeClasses = {
    sm: 'px-3 py-2 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg'
  };

  const variantClasses = {
    default: 'bg-blue-600 hover:bg-blue-700 text-white',
    kenya: `bg-[${colors.kenya.green}] hover:bg-green-700 text-white`,
    cultural: `bg-[${colors.cultural.gold}] hover:bg-yellow-600 text-white`,
    elite: 'bg-purple-600 hover:bg-purple-700 text-white'
  };

  return (
    <button
      onClick={onClick}
      disabled={disabled || loading}
      className={cn(
        'inline-flex items-center justify-center font-medium rounded-lg transition-colors duration-200',
        'disabled:opacity-50 disabled:cursor-not-allowed',
        sizeClasses[size],
        variantClasses[variant],
        className
      )}
    >
      {loading && (
        <LoadingSpinner
          size="sm"
          variant={variant}
          className="mr-2 text-white"
        />
      )}
      {children}
    </button>
  );
};

export default {
  LoadingSpinner,
  LoadingCard,
  VideoLoading,
  Skeleton,
  SkeletonCard,
  SkeletonTable,
  PageLoading,
  LoadingButton
};
