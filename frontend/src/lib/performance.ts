// [SNIPPET]: thinkwithai + kenyafirst + refactorclean + taskchain
// [CONTEXT]: Phase 3 - Performance optimization utilities for enterprise-grade SaaS
// [GOAL]: Advanced caching, lazy loading, and performance monitoring
// [TASK]: Implement comprehensive performance optimization strategies

'use client';

import { useEffect, useCallback, useRef, useState } from 'react';

// Advanced caching strategies
export class AdvancedCache {
  private cache = new Map<string, { data: any; timestamp: number; ttl: number }>();
  private maxSize = 100;

  set(key: string, data: any, ttl: number = 300000) { // 5 minutes default
    if (this.cache.size >= this.maxSize) {
      const firstKey = this.cache.keys().next().value;
      this.cache.delete(firstKey);
    }
    
    this.cache.set(key, {
      data,
      timestamp: Date.now(),
      ttl
    });
  }

  get(key: string) {
    const item = this.cache.get(key);
    if (!item) return null;

    if (Date.now() - item.timestamp > item.ttl) {
      this.cache.delete(key);
      return null;
    }

    return item.data;
  }

  clear() {
    this.cache.clear();
  }

  // Kenya-first cache warming for common data
  warmKenyaFirstData() {
    const kenyaData = {
      regions: ['Nairobi', 'Mombasa', 'Kisumu', 'Nakuru', 'Eldoret'],
      categories: ['Tourism 🦒', 'Culture 🎭', 'Business 💼', 'Education 📚'],
      colors: { primary: '#00A651', secondary: '#FFD700' }
    };
    this.set('kenya-first-data', kenyaData, 600000); // 10 minutes
  }
}

// Lazy loading hook with intersection observer
export const useLazyLoad = (threshold: number = 0.1) => {
  const elementRef = useRef<HTMLElement>(null);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
          observer.disconnect();
        }
      },
      { threshold }
    );

    if (elementRef.current) {
      observer.observe(elementRef.current);
    }

    return () => observer.disconnect();
  }, [threshold]);

  return { elementRef, isVisible };
};

// Performance monitoring
export class PerformanceMonitor {
  private metrics: { [key: string]: number } = {};

  startTiming(label: string) {
    this.metrics[`${label}_start`] = performance.now();
  }

  endTiming(label: string) {
    const startTime = this.metrics[`${label}_start`];
    if (startTime) {
      const duration = performance.now() - startTime;
      this.metrics[label] = duration;
      
      // Log slow operations (Kenya-first context)
      if (duration > 1000) {
        console.warn(`🇰🇪 Slow operation detected: ${label} took ${duration.toFixed(2)}ms`);
      }
      
      return duration;
    }
    return 0;
  }

  getMetrics() {
    return { ...this.metrics };
  }

  // Kenya-first performance reporting
  generateKenyaFirstReport() {
    const report = {
      timestamp: new Date().toISOString(),
      location: 'Kenya-First Platform',
      metrics: this.getMetrics(),
      recommendations: this.getRecommendations()
    };
    
    return report;
  }

  private getRecommendations() {
    const recommendations = [];
    
    Object.entries(this.metrics).forEach(([key, value]) => {
      if (key.endsWith('_start')) return;
      
      if (value > 2000) {
        recommendations.push(`🦒 Optimize ${key} - currently ${value.toFixed(2)}ms`);
      } else if (value < 100) {
        recommendations.push(`🦁 ${key} performing excellently - ${value.toFixed(2)}ms`);
      }
    });
    
    return recommendations;
  }
}

// Image optimization for Kenya-first content
export const optimizeKenyaImage = (src: string, width?: number, height?: number) => {
  const params = new URLSearchParams();
  if (width) params.set('w', width.toString());
  if (height) params.set('h', height.toString());
  params.set('q', '85'); // High quality for cultural content
  params.set('f', 'webp'); // Modern format
  
  return `${src}?${params.toString()}`;
};

// Code splitting utilities
export const loadComponent = async (componentPath: string) => {
  const perfMonitor = new PerformanceMonitor();
  perfMonitor.startTiming(`load_${componentPath}`);
  
  try {
    const component = await import(componentPath);
    perfMonitor.endTiming(`load_${componentPath}`);
    return component;
  } catch (error) {
    console.error(`🇰🇪 Failed to load component: ${componentPath}`, error);
    throw error;
  }
};

// Global cache instance
export const globalCache = new AdvancedCache();
export const perfMonitor = new PerformanceMonitor();

// Initialize Kenya-first optimizations
if (typeof window !== 'undefined') {
  globalCache.warmKenyaFirstData();
}
