// [SNIPPET]: thinkwithai + kenyafirst + refactorclean + taskchain
// [CONTEXT]: Phase 3 - Accessible button component with Kenya-first design
// [GOAL]: WCAG 2.1 AA compliant button with cultural authenticity
// [TASK]: Create enterprise-grade accessible button component

'use client';

import React, { forwardRef, ButtonHTMLAttributes } from 'react';
import { useAriaUtils, useAccessibilityPreferences } from '@/hooks/useAccessibility';
import LoadingStates from '@/components/ui/LoadingStates';

interface AccessibleButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'kenya';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  loadingText?: string;
  icon?: React.ReactNode;
  iconPosition?: 'left' | 'right';
  fullWidth?: boolean;
  ariaLabel?: string;
  ariaDescription?: string;
  culturalContext?: string;
}

const AccessibleButton = forwardRef<HTMLButtonElement, AccessibleButtonProps>(
  ({
    children,
    variant = 'primary',
    size = 'md',
    loading = false,
    loadingText,
    icon,
    iconPosition = 'left',
    fullWidth = false,
    ariaLabel,
    ariaDescription,
    culturalContext,
    className = '',
    disabled,
    ...props
  }, ref) => {
    const { createAriaLabel, createAriaDescription, generateId } = useAriaUtils();
    const { reduceMotion, highContrast } = useAccessibilityPreferences();

    const buttonId = generateId('btn');
    const descriptionId = ariaDescription ? generateId('desc') : undefined;

    // Kenya-first variant styles
    const getVariantStyles = () => {
      const baseStyles = 'font-medium transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2';
      
      if (highContrast) {
        return `${baseStyles} border-2 border-black text-black bg-white hover:bg-black hover:text-white`;
      }

      switch (variant) {
        case 'kenya':
          return `${baseStyles} bg-gradient-to-r from-green-600 to-green-700 text-white hover:from-green-700 hover:to-green-800 focus:ring-green-500 shadow-lg hover:shadow-xl`;
        case 'primary':
          return `${baseStyles} bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500`;
        case 'secondary':
          return `${baseStyles} bg-gray-600 text-white hover:bg-gray-700 focus:ring-gray-500`;
        case 'outline':
          return `${baseStyles} border border-gray-300 text-gray-700 hover:bg-gray-50 focus:ring-blue-500`;
        case 'ghost':
          return `${baseStyles} text-gray-700 hover:bg-gray-100 focus:ring-blue-500`;
        default:
          return `${baseStyles} bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500`;
      }
    };

    const getSizeStyles = () => {
      switch (size) {
        case 'sm':
          return 'px-3 py-1.5 text-sm min-h-[36px]'; // WCAG minimum touch target
        case 'lg':
          return 'px-6 py-3 text-lg min-h-[48px]';
        default:
          return 'px-4 py-2 text-base min-h-[44px]'; // Optimal touch target
      }
    };

    const getAnimationStyles = () => {
      if (reduceMotion) {
        return 'transition-none';
      }
      return 'transform hover:scale-105 active:scale-95';
    };

    const finalAriaLabel = ariaLabel || createAriaLabel(
      typeof children === 'string' ? children : 'Button',
      culturalContext
    );

    const finalAriaDescription = ariaDescription || createAriaDescription(
      `Activate ${typeof children === 'string' ? children : 'button'}`,
      culturalContext || 'Kenya-first platform action'
    );

    const buttonClasses = [
      getVariantStyles(),
      getSizeStyles(),
      getAnimationStyles(),
      fullWidth ? 'w-full' : '',
      disabled || loading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer',
      'inline-flex items-center justify-center gap-2',
      'rounded-md',
      className
    ].filter(Boolean).join(' ');

    return (
      <>
        <button
          ref={ref}
          id={buttonId}
          className={buttonClasses}
          disabled={disabled || loading}
          aria-label={finalAriaLabel}
          aria-describedby={descriptionId}
          aria-busy={loading}
          {...props}
        >
          {loading ? (
            <>
              <LoadingStates.LoadingSpinner size="sm" variant="kenya" />
              <span>{loadingText || 'Loading...'}</span>
            </>
          ) : (
            <>
              {icon && iconPosition === 'left' && (
                <span className="flex-shrink-0" aria-hidden="true">
                  {icon}
                </span>
              )}
              <span>{children}</span>
              {icon && iconPosition === 'right' && (
                <span className="flex-shrink-0" aria-hidden="true">
                  {icon}
                </span>
              )}
            </>
          )}
        </button>
        
        {descriptionId && (
          <div
            id={descriptionId}
            className="sr-only"
            aria-hidden="true"
          >
            {finalAriaDescription}
          </div>
        )}
      </>
    );
  }
);

AccessibleButton.displayName = 'AccessibleButton';

export default AccessibleButton;
