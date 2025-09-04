'use client';

import { ReactNode } from 'react';

// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorclean
// [CONTEXT]: Enterprise-grade card component with Kenya-first design system
// [GOAL]: Create beautiful, interactive cards with cultural authenticity
// [TASK]: Implement card with proper styling, hover effects, and variants

interface CardProps {
  children: ReactNode;
  className?: string;
  variant?: 'default' | 'elite' | 'cultural' | 'glass';
  hover?: boolean;
  padding?: 'sm' | 'md' | 'lg' | 'xl';
}

export default function Card({
  children,
  className = '',
  variant = 'default',
  hover = true,
  padding = 'lg'
}: CardProps) {
  const baseClasses = 'rounded-xl transition-all duration-300';

  const variantClasses = {
    default: 'bg-white border border-gray-200 shadow-sm',
    elite: 'elite-card',
    cultural: 'bg-gradient-to-br from-yellow-50 to-orange-50 border border-yellow-200 shadow-cultural',
    glass: 'glass-effect'
  };

  const paddingClasses = {
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8',
    xl: 'p-10'
  };

  const hoverClasses = hover ? 'hover-lift' : '';

  const combinedClasses = [
    baseClasses,
    variantClasses[variant],
    paddingClasses[padding],
    hoverClasses,
    className
  ].filter(Boolean).join(' ');

  return (
    <div className={combinedClasses}>
      {children}
    </div>
  );
}
