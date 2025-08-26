// [SNIPPET]: thinkwithai + surgicalfix + refactorintent + augmentsearch
// [CONTEXT]: Utility functions for production-ready application
// [GOAL]: Create comprehensive utility functions for performance and UX
// [TASK]: Implement utilities for caching, performance monitoring, and user experience

import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

// Utility for merging Tailwind classes
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// Performance monitoring utilities
export class PerformanceMonitor {
  private static instance: PerformanceMonitor;
  private metrics: Map<string, number> = new Map();

  static getInstance(): PerformanceMonitor {
    if (!PerformanceMonitor.instance) {
      PerformanceMonitor.instance = new PerformanceMonitor();
    }
    return PerformanceMonitor.instance;
  }

  startTiming(label: string): void {
    this.metrics.set(label, performance.now());
  }

  endTiming(label: string): number {
    const startTime = this.metrics.get(label);
    if (!startTime) return 0;
    
    const duration = performance.now() - startTime;
    this.metrics.delete(label);
    
    // Log in development
    if (process.env.NODE_ENV === 'development') {
      console.log(`⏱️ ${label}: ${duration.toFixed(2)}ms`);
    }
    
    return duration;
  }

  measureAsync<T>(label: string, fn: () => Promise<T>): Promise<T> {
    this.startTiming(label);
    return fn().finally(() => this.endTiming(label));
  }
}

// Local storage utilities with error handling
export const storage = {
  get<T>(key: string, defaultValue: T): T {
    try {
      const item = localStorage.getItem(key);
      return item ? JSON.parse(item) : defaultValue;
    } catch (error) {
      console.warn(`Failed to get ${key} from localStorage:`, error);
      return defaultValue;
    }
  },

  set<T>(key: string, value: T): boolean {
    try {
      localStorage.setItem(key, JSON.stringify(value));
      return true;
    } catch (error) {
      console.warn(`Failed to set ${key} in localStorage:`, error);
      return false;
    }
  },

  remove(key: string): boolean {
    try {
      localStorage.removeItem(key);
      return true;
    } catch (error) {
      console.warn(`Failed to remove ${key} from localStorage:`, error);
      return false;
    }
  },

  clear(): boolean {
    try {
      localStorage.clear();
      return true;
    } catch (error) {
      console.warn('Failed to clear localStorage:', error);
      return false;
    }
  }
};

// Debounce utility for performance
export function debounce<T extends (...args: unknown[]) => unknown>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout;
  return (...args: Parameters<T>) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
}

// Throttle utility for performance
export function throttle<T extends (...args: unknown[]) => unknown>(
  func: T,
  limit: number
): (...args: Parameters<T>) => void {
  let inThrottle: boolean;
  return (...args: Parameters<T>) => {
    if (!inThrottle) {
      func(...args);
      inThrottle = true;
      setTimeout(() => (inThrottle = false), limit);
    }
  };
}

// Format utilities
export const formatters = {
  currency: (amount: number, currency = 'KES'): string => {
    return new Intl.NumberFormat('en-KE', {
      style: 'currency',
      currency,
    }).format(amount);
  },

  number: (num: number): string => {
    return new Intl.NumberFormat('en-KE').format(num);
  },

  date: (date: Date | string, options?: Intl.DateTimeFormatOptions): string => {
    const dateObj = typeof date === 'string' ? new Date(date) : date;
    return new Intl.DateTimeFormat('en-KE', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      ...options,
    }).format(dateObj);
  },

  relativeTime: (date: Date | string): string => {
    const dateObj = typeof date === 'string' ? new Date(date) : date;
    const now = new Date();
    const diffInSeconds = Math.floor((now.getTime() - dateObj.getTime()) / 1000);

    if (diffInSeconds < 60) return 'just now';
    if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)} minutes ago`;
    if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)} hours ago`;
    if (diffInSeconds < 2592000) return `${Math.floor(diffInSeconds / 86400)} days ago`;
    
    return formatters.date(dateObj);
  },

  fileSize: (bytes: number): string => {
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    if (bytes === 0) return '0 Bytes';
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i];
  }
};

// Validation utilities
export const validators = {
  email: (email: string): boolean => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  },

  phone: (phone: string): boolean => {
    // Kenya phone number validation
    const phoneRegex = /^(\+254|0)[17]\d{8}$/;
    return phoneRegex.test(phone.replace(/\s/g, ''));
  },

  url: (url: string): boolean => {
    try {
      new URL(url);
      return true;
    } catch {
      return false;
    }
  },

  required: (value: unknown): boolean => {
    if (typeof value === 'string') return value.trim().length > 0;
    if (Array.isArray(value)) return value.length > 0;
    return value !== null && value !== undefined;
  }
};

// Device detection utilities
export const device = {
  isMobile: (): boolean => {
    if (typeof navigator === 'undefined') return false;
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
      navigator.userAgent
    );
  },

  isIOS: (): boolean => {
    if (typeof navigator === 'undefined') return false;
    return /iPad|iPhone|iPod/.test(navigator.userAgent);
  },

  isAndroid: (): boolean => {
    if (typeof navigator === 'undefined') return false;
    return /Android/.test(navigator.userAgent);
  },

  isTouchDevice: (): boolean => {
    if (typeof window === 'undefined' || typeof navigator === 'undefined') return false;
    return 'ontouchstart' in window || navigator.maxTouchPoints > 0;
  },

  getViewportSize: (): { width: number; height: number } => {
    if (typeof window === 'undefined') {
      return { width: 0, height: 0 };
    }
    return {
      width: window.innerWidth,
      height: window.innerHeight,
    };
  }
};

// Error reporting utility
export function reportError(error: Error, context?: Record<string, unknown>): void {
  if (process.env.NODE_ENV === 'development') {
    console.error('Error reported:', error, context);
  } else {
    // In production, send to error monitoring service
    // e.g., Sentry, LogRocket, etc.
    console.error('Production error:', error.message);
  }
}

// Feature flag utility
export function isFeatureEnabled(feature: string): boolean {
  // In a real app, this would check against a feature flag service
  const features = storage.get<Record<string, boolean>>('features', {} as Record<string, boolean>);
  return features[feature] === true;
}

// Analytics utility
export const analytics = {
  track: (event: string, properties?: Record<string, unknown>): void => {
    if (process.env.NODE_ENV === 'development') {
      console.log('📊 Analytics:', event, properties);
    } else {
      // In production, send to analytics service
      // e.g., Google Analytics, Mixpanel, etc.
    }
  },

  page: (page: string, properties?: Record<string, unknown>): void => {
    analytics.track('page_view', { page, ...properties });
  },

  user: (userId: string, properties?: Record<string, unknown>): void => {
    analytics.track('user_identify', { userId, ...properties });
  }
};

// Kenya-specific utilities
export const kenya = {
  counties: [
    'Baringo', 'Bomet', 'Bungoma', 'Busia', 'Elgeyo-Marakwet', 'Embu',
    'Garissa', 'Homa Bay', 'Isiolo', 'Kajiado', 'Kakamega', 'Kericho',
    'Kiambu', 'Kilifi', 'Kirinyaga', 'Kisii', 'Kisumu', 'Kitui',
    'Kwale', 'Laikipia', 'Lamu', 'Machakos', 'Makueni', 'Mandera',
    'Marsabit', 'Meru', 'Migori', 'Mombasa', 'Murang\'a', 'Nairobi',
    'Nakuru', 'Nandi', 'Narok', 'Nyamira', 'Nyandarua', 'Nyeri',
    'Samburu', 'Siaya', 'Taita-Taveta', 'Tana River', 'Tharaka-Nithi',
    'Trans Nzoia', 'Turkana', 'Uasin Gishu', 'Vihiga', 'Wajir', 'West Pokot'
  ],

  languages: [
    'English', 'Kiswahili', 'Kikuyu', 'Luo', 'Luhya', 'Kamba',
    'Kisii', 'Meru', 'Mijikenda', 'Turkana', 'Maasai', 'Sheng'
  ],

  formatPhoneNumber: (phone: string): string => {
    const cleaned = phone.replace(/\D/g, '');
    if (cleaned.startsWith('254')) {
      return `+${cleaned}`;
    }
    if (cleaned.startsWith('0')) {
      return `+254${cleaned.slice(1)}`;
    }
    return phone;
  }
};

export default {
  cn,
  PerformanceMonitor,
  storage,
  debounce,
  throttle,
  formatters,
  validators,
  device,
  reportError,
  isFeatureEnabled,
  analytics,
  kenya
};
