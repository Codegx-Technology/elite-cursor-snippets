'use client';

import { useState, useEffect, useRef } from 'react';
import { optimizeKenyaImage, perfMonitor } from '@/lib/performance';
import LoadingStates from '@/components/ui/LoadingStates';

interface LazyImageProps {
  src: string;
  alt: string;
  placeholder?: React.ReactNode;
  className?: string;
  width?: number;
  height?: number;
  priority?: boolean;
}

const LazyImage: React.FC<LazyImageProps> = ({ 
  src, 
  alt, 
  placeholder, 
  className, 
  width, 
  height, 
  priority = false 
}) => {
  const [inView, setInView] = useState(priority); // Load immediately if priority
  const [isLoaded, setIsLoaded] = useState(false);
  const [error, setError] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (priority) return; // Skip observer for priority images
    
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setInView(true);
          observer.disconnect();
        }
      },
      { rootMargin: '100px' } // Pre-load images 100px before they enter the viewport
    );

    if (ref.current) {
      observer.observe(ref.current);
    }

    return () => {
      if (ref.current) {
        observer.unobserve(ref.current);
      }
    };
  }, [priority]);

  useEffect(() => {
    if (inView) {
      perfMonitor.startTiming(`image_load_${alt}`);
      
      const img = new Image();
      const optimizedSrc = optimizeKenyaImage(src, width, height);
      img.src = optimizedSrc;
      
      img.onload = () => {
        setIsLoaded(true);
        perfMonitor.endTiming(`image_load_${alt}`);
      };
      
      img.onerror = () => {
        setError(true);
        perfMonitor.endTiming(`image_load_${alt}`);
        console.error(`🇰🇪 Failed to load image: ${src}`);
      };
    }
  }, [inView, src, alt, width, height]);

  const defaultPlaceholder = (
    <div className="flex items-center justify-center bg-gray-100 animate-pulse">
      <LoadingStates.LoadingSpinner size="sm" variant="kenya" />
    </div>
  );

  const errorPlaceholder = (
    <div className="flex items-center justify-center bg-gray-100 text-gray-500">
      <span className="text-sm">🇰🇪 Image unavailable</span>
    </div>
  );

  return (
    <div ref={ref} className={className}>
      {error ? (
        errorPlaceholder
      ) : isLoaded ? (
        <img 
          src={optimizeKenyaImage(src, width, height)} 
          alt={alt} 
          className="w-full h-full object-cover transition-opacity duration-300" 
          loading={priority ? 'eager' : 'lazy'}
        />
      ) : (
        placeholder || defaultPlaceholder
      )}
    </div>
  );
};

export default LazyImage;
