// [SNIPPET]: thinkwithai + kenyafirst + refactorclean + taskchain
// [CONTEXT]: Enterprise-grade Dashboard Layout with Kenya-first design system integration
// [GOAL]: Create flexible dashboard layout components with cultural authenticity
// [TASK]: Phase 2.1c - Dashboard layout components with cultural design patterns

'use client';

import React from 'react';
import { colors, spacing, typography } from '@/config/designTokens';
import { cn } from '@/lib/utils';

// Dashboard Grid System
export interface DashboardGridProps {
  children: React.ReactNode;
  variant?: 'default' | 'kenya' | 'cultural' | 'elite';
  className?: string;
  cols?: 1 | 2 | 3 | 4;
  gap?: 'sm' | 'md' | 'lg';
}

export const DashboardGrid: React.FC<DashboardGridProps> = ({
  children,
  variant = 'default',
  className,
  cols = 3,
  gap = 'md'
}) => {
  const gapClasses = {
    sm: 'gap-4',
    md: 'gap-6',
    lg: 'gap-8'
  };

  const colClasses = {
    1: 'grid-cols-1',
    2: 'grid-cols-1 md:grid-cols-2',
    3: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3',
    4: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-4'
  };

  return (
    <div className={cn(
      'grid',
      colClasses[cols],
      gapClasses[gap],
      'w-full',
      className
    )}>
      {children}
    </div>
  );
};

// Dashboard Card Component
export interface DashboardCardProps {
  children: React.ReactNode;
  title?: string;
  subtitle?: string;
  variant?: 'default' | 'kenya' | 'cultural' | 'elite';
  className?: string;
  headerAction?: React.ReactNode;
  padding?: 'sm' | 'md' | 'lg';
}

export const DashboardCard: React.FC<DashboardCardProps> = ({
  children,
  title,
  subtitle,
  variant = 'default',
  className,
  headerAction,
  padding = 'md'
}) => {
  const variantClasses = {
    default: 'border-gray-200 bg-white',
    kenya: `border-[${colors.kenya.green}] border-opacity-20 bg-white`,
    cultural: `border-[${colors.cultural.gold}] border-opacity-30 bg-gradient-to-br from-white to-yellow-50`,
    elite: 'border-purple-200 bg-gradient-to-br from-white to-purple-50'
  };

  const paddingClasses = {
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8'
  };

  return (
    <div className={cn(
      'rounded-lg border shadow-sm transition-all duration-200 hover:shadow-md',
      variantClasses[variant],
      paddingClasses[padding],
      className
    )}>
      {(title || subtitle || headerAction) && (
        <div className="flex items-start justify-between mb-4">
          <div>
            {title && (
              <h3 className={cn(
                'font-semibold text-gray-900',
                `text-[${typography.fontSizes.lg}]`,
                variant === 'kenya' && `text-[${colors.kenya.green}]`,
                variant === 'cultural' && `text-[${colors.cultural.gold}]`
              )}>
                {title}
              </h3>
            )}
            {subtitle && (
              <p className={cn(
                'text-gray-600 mt-1',
                `text-[${typography.fontSizes.sm}]`
              )}>
                {subtitle}
              </p>
            )}
          </div>
          {headerAction && (
            <div className="flex-shrink-0">
              {headerAction}
            </div>
          )}
        </div>
      )}
      {children}
    </div>
  );
};

// Metric Card Component
export interface MetricCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  trend?: {
    value: number;
    isPositive: boolean;
    label?: string;
  };
  variant?: 'default' | 'kenya' | 'cultural' | 'elite';
  icon?: React.ReactNode;
  className?: string;
}

export const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  subtitle,
  trend,
  variant = 'default',
  icon,
  className
}) => {
  const variantClasses = {
    default: 'border-gray-200 bg-white',
    kenya: `border-[${colors.kenya.green}] border-opacity-20 bg-green-50`,
    cultural: `border-[${colors.cultural.gold}] border-opacity-30 bg-yellow-50`,
    elite: 'border-purple-200 bg-purple-50'
  };

  const iconColors = {
    default: 'text-blue-500',
    kenya: `text-[${colors.kenya.green}]`,
    cultural: `text-[${colors.cultural.gold}]`,
    elite: 'text-purple-500'
  };

  const valueColors = {
    default: 'text-gray-900',
    kenya: 'text-green-700',
    cultural: 'text-yellow-700',
    elite: 'text-purple-700'
  };

  return (
    <DashboardCard
      variant={variant}
      className={cn(variantClasses[variant], className)}
      padding="md"
    >
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center space-x-2 mb-2">
            {icon && (
              <div className={cn('text-xl', iconColors[variant])}>
                {icon}
              </div>
            )}
            <h4 className={cn(
              'font-medium text-gray-600',
              `text-[${typography.fontSizes.sm}]`
            )}>
              {title}
            </h4>
          </div>
          
          <div className={cn(
            'font-bold mb-1',
            `text-[${typography.fontSizes['3xl']}]`,
            valueColors[variant]
          )}>
            {typeof value === 'number' ? value.toLocaleString() : value}
          </div>
          
          {subtitle && (
            <p className={cn(
              'text-gray-500',
              `text-[${typography.fontSizes.xs}]`
            )}>
              {subtitle}
            </p>
          )}
        </div>
        
        {trend && (
          <div className={cn(
            'flex items-center space-x-1 px-2 py-1 rounded-full text-xs font-medium',
            trend.isPositive 
              ? 'bg-green-100 text-green-700' 
              : 'bg-red-100 text-red-700'
          )}>
            <span>{trend.isPositive ? '↗' : '↘'}</span>
            <span>{Math.abs(trend.value)}%</span>
            {trend.label && <span>{trend.label}</span>}
          </div>
        )}
      </div>
    </DashboardCard>
  );
};

// Dashboard Header Component
export interface DashboardHeaderProps {
  title: string;
  subtitle?: string;
  variant?: 'default' | 'kenya' | 'cultural' | 'elite';
  actions?: React.ReactNode;
  breadcrumbs?: Array<{
    label: string;
    href?: string;
  }>;
  className?: string;
}

export const DashboardHeader: React.FC<DashboardHeaderProps> = ({
  title,
  subtitle,
  variant = 'default',
  actions,
  breadcrumbs,
  className
}) => {
  const titleColors = {
    default: 'text-gray-900',
    kenya: `text-[${colors.kenya.green}]`,
    cultural: `text-[${colors.cultural.gold}]`,
    elite: 'text-purple-700'
  };

  return (
    <div className={cn('mb-8', className)}>
      {breadcrumbs && (
        <nav className="mb-4">
          <ol className="flex items-center space-x-2 text-sm text-gray-500">
            {breadcrumbs.map((crumb, index) => (
              <li key={index} className="flex items-center">
                {index > 0 && <span className="mx-2">/</span>}
                {crumb.href ? (
                  <a href={crumb.href} className="hover:text-gray-700">
                    {crumb.label}
                  </a>
                ) : (
                  <span className="text-gray-900">{crumb.label}</span>
                )}
              </li>
            ))}
          </ol>
        </nav>
      )}
      
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-4 sm:space-y-0">
        <div>
          <h1 className={cn(
            'font-bold',
            `text-[${typography.fontSizes['3xl']}]`,
            titleColors[variant]
          )}>
            {title}
          </h1>
          {subtitle && (
            <p className={cn(
              'text-gray-600 mt-2',
              `text-[${typography.fontSizes.base}]`
            )}>
              {subtitle}
            </p>
          )}
        </div>
        
        {actions && (
          <div className="flex items-center space-x-3">
            {actions}
          </div>
        )}
      </div>
    </div>
  );
};

// Dashboard Section Component
export interface DashboardSectionProps {
  children: React.ReactNode;
  title?: string;
  subtitle?: string;
  variant?: 'default' | 'kenya' | 'cultural' | 'elite';
  className?: string;
  headerAction?: React.ReactNode;
}

export const DashboardSection: React.FC<DashboardSectionProps> = ({
  children,
  title,
  subtitle,
  variant = 'default',
  className,
  headerAction
}) => {
  const titleColors = {
    default: 'text-gray-900',
    kenya: `text-[${colors.kenya.green}]`,
    cultural: `text-[${colors.cultural.gold}]`,
    elite: 'text-purple-700'
  };

  return (
    <section className={cn('mb-8', className)}>
      {(title || subtitle || headerAction) && (
        <div className="flex items-start justify-between mb-6">
          <div>
            {title && (
              <h2 className={cn(
                'font-semibold',
                `text-[${typography.fontSizes['2xl']}]`,
                titleColors[variant]
              )}>
                {title}
              </h2>
            )}
            {subtitle && (
              <p className={cn(
                'text-gray-600 mt-1',
                `text-[${typography.fontSizes.base}]`
              )}>
                {subtitle}
              </p>
            )}
          </div>
          {headerAction && (
            <div className="flex-shrink-0">
              {headerAction}
            </div>
          )}
        </div>
      )}
      {children}
    </section>
  );
};

// Export all dashboard components
export {
  DashboardGrid as Grid,
  DashboardCard as Card,
  MetricCard as Metric,
  DashboardHeader as Header,
  DashboardSection as Section
};
