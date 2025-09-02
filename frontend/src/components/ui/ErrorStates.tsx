// [SNIPPET]: thinkwithai + kenyafirst + refactorclean + taskchain
// [CONTEXT]: Enterprise-grade error states with Kenya-first design system integration
// [GOAL]: Comprehensive error UI components with cultural authenticity and user-friendly messaging
// [TASK]: Phase 2.3 - Error & Loading States with comprehensive state management UI

'use client';

import React from 'react';
import { colors, spacing, typography } from '@/config/designTokens';
import { cn } from '@/lib/utils';
import { FaExclamationTriangle, FaTimesCircle, FaInfoCircle, FaCheckCircle, FaRedo, FaHome } from 'react-icons/fa6';

// Alert Component
export interface AlertProps {
  type?: 'success' | 'error' | 'warning' | 'info';
  title?: string;
  message: string;
  variant?: 'default' | 'kenya' | 'cultural' | 'elite';
  className?: string;
  onClose?: () => void;
  actions?: React.ReactNode;
}

export const Alert: React.FC<AlertProps> = ({
  type = 'info',
  title,
  message,
  variant = 'default',
  className,
  onClose,
  actions
}) => {
  const typeConfig = {
    success: {
      icon: <FaCheckCircle className="w-5 h-5" />,
      colors: 'bg-green-50 border-green-200 text-green-800',
      iconColor: 'text-green-600'
    },
    error: {
      icon: <FaTimesCircle className="w-5 h-5" />,
      colors: 'bg-red-50 border-red-200 text-red-800',
      iconColor: 'text-red-600'
    },
    warning: {
      icon: <FaExclamationTriangle className="w-5 h-5" />,
      colors: 'bg-yellow-50 border-yellow-200 text-yellow-800',
      iconColor: 'text-yellow-600'
    },
    info: {
      icon: <FaInfoCircle className="w-5 h-5" />,
      colors: 'bg-blue-50 border-blue-200 text-blue-800',
      iconColor: 'text-blue-600'
    }
  };

  const config = typeConfig[type];

  return (
    <div className={cn(
      'rounded-lg border p-4',
      config.colors,
      className
    )}>
      <div className="flex items-start space-x-3">
        <div className={config.iconColor}>
          {config.icon}
        </div>
        
        <div className="flex-1 min-w-0">
          {title && (
            <h3 className={cn(
              'font-semibold mb-1',
              `text-[${typography.fontSizes.sm}]`
            )}>
              {title}
            </h3>
          )}
          <p className={cn(
            `text-[${typography.fontSizes.sm}]`
          )}>
            {message}
          </p>
          
          {actions && (
            <div className="mt-3">
              {actions}
            </div>
          )}
        </div>
        
        {onClose && (
          <button
            onClick={onClose}
            className="flex-shrink-0 text-gray-400 hover:text-gray-600 transition-colors"
          >
            <FaTimesCircle className="w-4 h-4" />
          </button>
        )}
      </div>
    </div>
  );
};

// Error Page Component
export interface ErrorPageProps {
  type?: 'not-found' | 'server-error' | 'network-error' | 'permission-denied';
  variant?: 'default' | 'kenya' | 'cultural' | 'elite';
  className?: string;
  onRetry?: () => void;
  onGoHome?: () => void;
  customTitle?: string;
  customMessage?: string;
}

export const ErrorPage: React.FC<ErrorPageProps> = ({
  type = 'server-error',
  variant = 'kenya',
  className,
  onRetry,
  onGoHome,
  customTitle,
  customMessage
}) => {
  const errorConfig = {
    'not-found': {
      title: 'Ukurasa Haujapatikana',
      message: 'Samahani, ukurasa unaotafuta haupo. Huenda umeondolewa au umebadilishwa.',
      icon: '🔍',
      code: '404'
    },
    'server-error': {
      title: 'Hitilafu ya Seva',
      message: 'Kuna tatizo la kiufundi. Tafadhali jaribu tena baada ya muda.',
      icon: '⚠️',
      code: '500'
    },
    'network-error': {
      title: 'Hakuna Muunganisho',
      message: 'Hakikisha una muunganisho wa mtandao na ujaribu tena.',
      icon: '📡',
      code: 'NET'
    },
    'permission-denied': {
      title: 'Hauruhusiwi',
      message: 'Huna ruhusa ya kufikia ukurasa huu. Wasiliana na msimamizi.',
      icon: '🔒',
      code: '403'
    }
  };

  const config = errorConfig[type];
  const title = customTitle || config.title;
  const message = customMessage || config.message;

  const variantClasses = {
    default: 'text-blue-600',
    kenya: `text-[${colors.kenya.green}]`,
    cultural: `text-[${colors.cultural.gold}]`,
    elite: 'text-purple-600'
  };

  return (
    <div className={cn(
      'min-h-screen flex items-center justify-center bg-gray-50 px-4',
      className
    )}>
      <div className="max-w-md w-full text-center">
        <div className="mb-8">
          <div className="text-6xl mb-4">{config.icon}</div>
          <div className={cn(
            'text-4xl font-bold mb-2',
            variantClasses[variant]
          )}>
            {config.code}
          </div>
          <h1 className={cn(
            'font-bold text-gray-900 mb-4',
            `text-[${typography.fontSizes['2xl']}]`
          )}>
            {title}
          </h1>
          <p className={cn(
            'text-gray-600 mb-8',
            `text-[${typography.fontSizes.base}]`
          )}>
            {message}
          </p>
        </div>

        <div className="space-y-3">
          {onRetry && (
            <button
              onClick={onRetry}
              className={cn(
                'w-full inline-flex items-center justify-center px-6 py-3 rounded-lg font-medium transition-colors',
                variant === 'kenya' ? `bg-[${colors.kenya.green}] hover:bg-green-700 text-white` :
                variant === 'cultural' ? `bg-[${colors.cultural.gold}] hover:bg-yellow-600 text-white` :
                variant === 'elite' ? 'bg-purple-600 hover:bg-purple-700 text-white' :
                'bg-blue-600 hover:bg-blue-700 text-white'
              )}
            >
              <FaRedo className="w-4 h-4 mr-2" />
              Jaribu Tena
            </button>
          )}
          
          {onGoHome && (
            <button
              onClick={onGoHome}
              className="w-full inline-flex items-center justify-center px-6 py-3 border border-gray-300 rounded-lg font-medium text-gray-700 bg-white hover:bg-gray-50 transition-colors"
            >
              <FaHome className="w-4 h-4 mr-2" />
              Rudi Nyumbani
            </button>
          )}
        </div>

        <div className="mt-8 text-xs text-gray-400">
          <p>Ikiwa tatizo linaendelea, wasiliana na timu ya msaada</p>
        </div>
      </div>
    </div>
  );
};

// Form Error Component
export interface FormErrorProps {
  errors: Record<string, string>;
  variant?: 'default' | 'kenya' | 'cultural' | 'elite';
  className?: string;
}

export const FormError: React.FC<FormErrorProps> = ({
  errors,
  variant = 'default',
  className
}) => {
  const errorEntries = Object.entries(errors).filter(([_, message]) => message);
  
  if (errorEntries.length === 0) return null;

  return (
    <div className={cn(
      'bg-red-50 border border-red-200 rounded-lg p-4',
      className
    )}>
      <div className="flex items-start space-x-3">
        <FaTimesCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
        <div className="flex-1">
          <h3 className={cn(
            'font-semibold text-red-800 mb-2',
            `text-[${typography.fontSizes.sm}]`
          )}>
            Kurekebisha Makosa
          </h3>
          <ul className="space-y-1">
            {errorEntries.map(([field, message]) => (
              <li key={field} className={cn(
                'text-red-700',
                `text-[${typography.fontSizes.sm}]`
              )}>
                • {message}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

// Empty State Component
export interface EmptyStateProps {
  title: string;
  message: string;
  icon?: React.ReactNode;
  variant?: 'default' | 'kenya' | 'cultural' | 'elite';
  className?: string;
  action?: {
    label: string;
    onClick: () => void;
  };
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  title,
  message,
  icon,
  variant = 'default',
  className,
  action
}) => {
  const variantClasses = {
    default: 'text-blue-600',
    kenya: `text-[${colors.kenya.green}]`,
    cultural: `text-[${colors.cultural.gold}]`,
    elite: 'text-purple-600'
  };

  const defaultIcon = (
    <div className={cn(
      'w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4',
      variant === 'kenya' ? 'bg-green-100' :
      variant === 'cultural' ? 'bg-yellow-100' :
      variant === 'elite' ? 'bg-purple-100' :
      'bg-gray-100'
    )}>
      <span className="text-2xl">📭</span>
    </div>
  );

  return (
    <div className={cn(
      'text-center py-12 px-4',
      className
    )}>
      {icon || defaultIcon}
      
      <h3 className={cn(
        'font-semibold text-gray-900 mb-2',
        `text-[${typography.fontSizes.lg}]`
      )}>
        {title}
      </h3>
      
      <p className={cn(
        'text-gray-600 mb-6 max-w-sm mx-auto',
        `text-[${typography.fontSizes.base}]`
      )}>
        {message}
      </p>

      {action && (
        <button
          onClick={action.onClick}
          className={cn(
            'inline-flex items-center px-4 py-2 rounded-lg font-medium transition-colors',
            variant === 'kenya' ? `bg-[${colors.kenya.green}] hover:bg-green-700 text-white` :
            variant === 'cultural' ? `bg-[${colors.cultural.gold}] hover:bg-yellow-600 text-white` :
            variant === 'elite' ? 'bg-purple-600 hover:bg-purple-700 text-white' :
            'bg-blue-600 hover:bg-blue-700 text-white'
          )}
        >
          {action.label}
        </button>
      )}
    </div>
  );
};

// Toast Notification Component
export interface ToastProps {
  type?: 'success' | 'error' | 'warning' | 'info';
  title?: string;
  message: string;
  variant?: 'default' | 'kenya' | 'cultural' | 'elite';
  duration?: number;
  onClose?: () => void;
}

export const Toast: React.FC<ToastProps> = ({
  type = 'info',
  title,
  message,
  variant = 'default',
  duration = 5000,
  onClose
}) => {
  React.useEffect(() => {
    if (duration > 0 && onClose) {
      const timer = setTimeout(onClose, duration);
      return () => clearTimeout(timer);
    }
  }, [duration, onClose]);

  const typeConfig = {
    success: {
      icon: <FaCheckCircle className="w-5 h-5" />,
      colors: 'bg-green-600 text-white',
      iconColor: 'text-green-200'
    },
    error: {
      icon: <FaTimesCircle className="w-5 h-5" />,
      colors: 'bg-red-600 text-white',
      iconColor: 'text-red-200'
    },
    warning: {
      icon: <FaExclamationTriangle className="w-5 h-5" />,
      colors: 'bg-yellow-600 text-white',
      iconColor: 'text-yellow-200'
    },
    info: {
      icon: <FaInfoCircle className="w-5 h-5" />,
      colors: 'bg-blue-600 text-white',
      iconColor: 'text-blue-200'
    }
  };

  const config = typeConfig[type];

  return (
    <div className={cn(
      'rounded-lg shadow-lg p-4 max-w-sm w-full',
      config.colors
    )}>
      <div className="flex items-start space-x-3">
        <div className={config.iconColor}>
          {config.icon}
        </div>
        
        <div className="flex-1 min-w-0">
          {title && (
            <h4 className={cn(
              'font-semibold mb-1',
              `text-[${typography.fontSizes.sm}]`
            )}>
              {title}
            </h4>
          )}
          <p className={cn(
            `text-[${typography.fontSizes.sm}]`,
            'opacity-90'
          )}>
            {message}
          </p>
        </div>
        
        {onClose && (
          <button
            onClick={onClose}
            className="flex-shrink-0 text-white opacity-70 hover:opacity-100 transition-opacity"
          >
            <FaTimesCircle className="w-4 h-4" />
          </button>
        )}
      </div>
    </div>
  );
};

// Network Status Component
export interface NetworkStatusProps {
  isOnline: boolean;
  variant?: 'default' | 'kenya' | 'cultural' | 'elite';
  className?: string;
}

export const NetworkStatus: React.FC<NetworkStatusProps> = ({
  isOnline,
  variant = 'default',
  className
}) => {
  if (isOnline) return null;

  return (
    <div className={cn(
      'fixed top-0 left-0 right-0 z-50 bg-red-600 text-white text-center py-2',
      className
    )}>
      <div className="flex items-center justify-center space-x-2">
        <span className="text-sm">📡</span>
        <span className={`text-[${typography.fontSizes.sm}]`}>
          Hakuna muunganisho wa mtandao
        </span>
      </div>
    </div>
  );
};

export default {
  Alert,
  ErrorPage,
  FormError,
  EmptyState,
  Toast,
  NetworkStatus
};

