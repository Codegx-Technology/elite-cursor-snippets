// [SNIPPET]: thinkwithai + kenyafirst + refactorclean + taskchain
// [CONTEXT]: Enterprise-grade design system component with Kenya-first cultural authenticity
// [GOAL]: Centralized design system utilities for consistent component styling

import React from 'react';
import { colors, spacing, typography, borderRadius, shadows } from '@/config/designTokens';
import { cn } from '@/lib/utils';

// Design System Component Variants
export interface DesignSystemProps {
  variant?: 'primary' | 'secondary' | 'kenya' | 'cultural' | 'danger' | 'success';
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
  className?: string;
  children?: React.ReactNode;
}

// Button Component with Design System Integration
export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement>, DesignSystemProps {
  loading?: boolean;
  icon?: React.ReactNode;
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ variant = 'primary', size = 'md', className, loading, icon, children, disabled, ...props }, ref) => {
    const baseClasses = 'inline-flex items-center justify-center font-semibold rounded-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed';
    
    const variantClasses = {
      primary: 'bg-gradient-to-r from-blue-600 to-purple-600 text-white hover:from-blue-700 hover:to-purple-700 focus:ring-blue-500 shadow-md hover:shadow-lg',
      secondary: 'bg-gray-200 text-gray-700 hover:bg-gray-300 focus:ring-gray-500',
      kenya: `bg-[${colors.kenya.green}] text-white hover:bg-green-700 focus:ring-green-500 shadow-kenya`,
      cultural: `bg-[${colors.cultural.gold}] text-gray-900 hover:bg-yellow-500 focus:ring-yellow-500 shadow-cultural`,
      danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500',
      success: 'bg-green-600 text-white hover:bg-green-700 focus:ring-green-500',
    };

    const sizeClasses = {
      xs: `px-2 py-1 text-xs`,
      sm: `px-3 py-2 text-sm`,
      md: `px-4 py-3 text-base`,
      lg: `px-5 py-4 text-lg`,
      xl: `px-8 py-5 text-${typography.fontSizes.xl}`,
    };

    return (
      <button
        ref={ref}
        className={cn(
          baseClasses,
          variantClasses[variant],
          sizeClasses[size],
          loading && 'cursor-wait',
          className
        )}
        disabled={disabled || loading}
        {...props}
      >
        {loading && (
          <svg className="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
          </svg>
        )}
        {icon && <span className="mr-2">{icon}</span>}
        {children}
      </button>
    );
  }
);
Button.displayName = 'Button';

// Card Component with Design System Integration
export interface CardProps extends React.HTMLAttributes<HTMLDivElement>, DesignSystemProps {
  padding?: keyof typeof spacing;
  shadow?: keyof typeof shadows;
}

export const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ variant = 'primary', size = 'md', padding = 'lg', shadow = 'md', className, children, ...props }, ref) => {
    const baseClasses = 'bg-white rounded-lg border transition-all duration-300';
    
    const variantClasses = {
      primary: 'border-gray-200 hover:border-blue-300',
      secondary: 'border-gray-300',
      kenya: `border-[${colors.kenya.green}] border-opacity-20`,
      cultural: `border-[${colors.cultural.gold}] border-opacity-30`,
      danger: 'border-red-200',
      success: 'border-green-200',
    };

    const paddingClass = `p-[${spacing[padding]}]`;
    const shadowClass = `shadow-${shadow}`;

    return (
      <div
        ref={ref}
        className={cn(
          baseClasses,
          variantClasses[variant],
          paddingClass,
          shadowClass,
          'hover:shadow-lg hover:-translate-y-1',
          className
        )}
        {...props}
      >
        {children}
      </div>
    );
  }
);
Card.displayName = 'Card';

// Input Component with Design System Integration
export interface InputProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'size'>, DesignSystemProps {
  label?: string;
  error?: string;
  helperText?: string;
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ variant = 'primary', size = 'md', label, error, helperText, className, ...props }, ref) => {
    const baseClasses = 'w-full border rounded-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-1';
    
    const variantClasses = {
      primary: 'border-gray-300 focus:border-blue-500 focus:ring-blue-500',
      secondary: 'border-gray-400 focus:border-gray-600 focus:ring-gray-500',
      kenya: `border-gray-300 focus:border-[${colors.kenya.green}] focus:ring-green-500`,
      cultural: `border-gray-300 focus:border-[${colors.cultural.gold}] focus:ring-yellow-500`,
      danger: 'border-red-300 focus:border-red-500 focus:ring-red-500',
      success: 'border-green-300 focus:border-green-500 focus:ring-green-500',
    };

    const sizeClasses = {
      xs: `px-2 py-1 text-${typography.fontSizes.xs}`,
      sm: `px-3 py-2 text-${typography.fontSizes.sm}`,
      md: `px-4 py-3 text-${typography.fontSizes.base}`,
      lg: `px-5 py-4 text-${typography.fontSizes.lg}`,
      xl: `px-6 py-5 text-${typography.fontSizes.xl}`,
    };

    const errorClasses = error ? 'border-red-500 focus:border-red-500 focus:ring-red-500' : '';

    return (
      <div className="w-full">
        {label && (
          <label className={`block text-${typography.fontSizes.sm} font-${typography.fontWeights.medium} text-gray-700 mb-2`}>
            {label}
          </label>
        )}
        <input
          ref={ref}
          className={cn(
            baseClasses,
            variantClasses[variant],
            sizeClasses[size],
            errorClasses,
            className
          )}
          {...props}
        />
        {error && (
          <p className={`mt-1 text-${typography.fontSizes.sm} text-red-600`}>{error}</p>
        )}
        {helperText && !error && (
          <p className={`mt-1 text-${typography.fontSizes.sm} text-gray-500`}>{helperText}</p>
        )}
      </div>
    );
  }
);
Input.displayName = 'Input';

// Typography Components
export interface TypographyProps extends React.HTMLAttributes<HTMLElement> {
  variant?: 'h1' | 'h2' | 'h3' | 'h4' | 'h5' | 'h6' | 'body' | 'caption';
  weight?: keyof typeof typography.fontWeights;
  color?: 'primary' | 'secondary' | 'kenya' | 'cultural' | 'muted';
}

export const Typography = React.forwardRef<HTMLElement, TypographyProps>(
  ({ variant = 'body', weight = 'normal', color = 'primary', className, children, ...props }, ref) => {
    const variantConfig = {
      h1: { tag: 'h1', size: typography.fontSizes['4xl'], weight: 'bold' },
      h2: { tag: 'h2', size: typography.fontSizes['3xl'], weight: 'bold' },
      h3: { tag: 'h3', size: typography.fontSizes['2xl'], weight: 'semibold' },
      h4: { tag: 'h4', size: typography.fontSizes.xl, weight: 'semibold' },
      h5: { tag: 'h5', size: typography.fontSizes.lg, weight: 'semibold' },
      h6: { tag: 'h6', size: typography.fontSizes.base, weight: 'semibold' },
      body: { tag: 'p', size: typography.fontSizes.base, weight: 'normal' },
      caption: { tag: 'span', size: typography.fontSizes.sm, weight: 'normal' },
    };

    const colorClasses = {
      primary: 'text-gray-900',
      secondary: 'text-gray-600',
      kenya: `text-[${colors.kenya.green}]`,
      cultural: `text-[${colors.cultural.gold}]`,
      muted: 'text-gray-500',
    };

    const config = variantConfig[variant];
    const Component = config.tag as React.ElementType;

    return (
      <Component
        ref={ref as any}
        className={cn(
          colorClasses[color],
          'leading-normal',
          className
        )}
        style={{
          fontSize: config.size,
          fontWeight: typography.fontWeights[weight as keyof typeof typography.fontWeights]
        }}
        {...props}
      >
        {children}
      </Component>
    );
  }
);
Typography.displayName = 'Typography';

// Export design tokens for direct usage
export { colors, spacing, typography, borderRadius, shadows };
