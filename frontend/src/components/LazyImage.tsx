'use client';

import Image from 'next/image';
import React from 'react'; // Import React for React.ReactNode

interface LazyImageProps {
  src: string;
  alt: string;
  placeholder?: React.ReactNode;
  className?: string;
  width: number; // Make required for next/image
  height: number; // Make required for next/image
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
  // next/image handles lazy loading, error states, and placeholders internally
  // The custom logic for IntersectionObserver, isLoaded, error states, and perfMonitor
  // related to image loading is now redundant.

  return (
    <Image
      src={src}
      alt={alt}
      className={className} // Pass className directly
      width={width}
      height={height}
      priority={priority}
      // next/image has its own error handling and placeholder mechanisms.
      // If custom placeholders/error states are needed, they should be implemented
      // using next/image's onError and onLoadingComplete props, or by wrapping
      // the Image component with custom logic.
    />
  );
};

export default LazyImage;
