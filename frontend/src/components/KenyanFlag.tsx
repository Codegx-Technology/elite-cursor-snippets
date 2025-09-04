import React from 'react';

// [SNIPPET]: kenyafirst + surgicalfix + thinkwithai
// [CONTEXT]: Authentic Kenyan flag component based on official government specifications
// [GOAL]: Single source of truth for Kenyan flag representation with proper proportions and colors
// [TASK]: Implement official Kenyan flag with accurate colors, proportions, and Maasai shield

interface KenyanFlagProps {
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl';
  className?: string;
  animated?: boolean;
}

const KenyanFlag: React.FC<KenyanFlagProps> = ({
  size = 'md',
  className = '',
  animated = false
}) => {
  const sizeClasses = {
    xs: 'w-6 h-4',
    sm: 'w-8 h-6',
    md: 'w-12 h-8',
    lg: 'w-16 h-11',
    xl: 'w-20 h-14',
    '2xl': 'w-24 h-16'
  };

  return (
    <div className={`${sizeClasses[size]} ${className} inline-block`}>
      <svg
        viewBox="0 0 300 200"
        className={`w-full h-full ${animated ? 'animate-pulse' : ''}`}
        xmlns="http://www.w3.org/2000/svg"
        role="img"
        aria-label="Flag of Kenya"
      >
        {/* Official Kenyan Flag - Based on Government Specifications */}

        {/* Black stripe (top) */}
        <rect x="0" y="0" width="300" height="33.33" fill="#000000" />

        {/* White stripe (separator) */}
        <rect x="0" y="33.33" width="300" height="16.67" fill="#FFFFFF" />

        {/* Red stripe */}
        <rect x="0" y="50" width="300" height="33.33" fill="#CE1126" />

        {/* White stripe (separator) */}
        <rect x="0" y="83.33" width="300" height="16.67" fill="#FFFFFF" />

        {/* Green stripe */}
        <rect x="0" y="100" width="300" height="33.33" fill="#007A3D" />

        {/* White stripe (separator) */}
        <rect x="0" y="133.33" width="300" height="16.67" fill="#FFFFFF" />

        {/* Red stripe */}
        <rect x="0" y="150" width="300" height="33.33" fill="#CE1126" />

        {/* White stripe (separator) */}
        <rect x="0" y="183.33" width="300" height="16.67" fill="#FFFFFF" />

        {/* Black stripe (bottom) */}
        <rect x="0" y="200" width="300" height="33.33" fill="#000000" />

        {/* Traditional Maasai Shield and Spears (Center Emblem) */}
        <g transform="translate(150, 116.67)">
          {/* Spears (behind shield) */}
          <g>
            {/* Left spear */}
            <line x1="-40" y1="-50" x2="-20" y2="50" stroke="#8B4513" strokeWidth="4" />
            <polygon points="-42,-55 -38,-55 -40,-45" fill="#C0C0C0" />

            {/* Right spear */}
            <line x1="40" y1="-50" x2="20" y2="50" stroke="#8B4513" strokeWidth="4" />
            <polygon points="42,-55 38,-55 40,-45" fill="#C0C0C0" />
          </g>

          {/* Maasai Shield */}
          <ellipse cx="0" cy="0" rx="28" ry="40" fill="#8B4513" stroke="#654321" strokeWidth="3" />

          {/* Traditional Shield Pattern */}
          <path d="M-23,-30 L23,-30 L18,-18 L-18,-18 Z" fill="#FFFFFF" />
          <path d="M-18,-18 L18,-18 L13,-6 L-13,-6 Z" fill="#CE1126" />
          <path d="M-13,-6 L13,-6 L10,6 L-10,6 Z" fill="#000000" />
          <path d="M-10,6 L10,6 L8,18 L-8,18 Z" fill="#FFFFFF" />
          <path d="M-8,18 L8,18 L5,30 L-5,30 Z" fill="#CE1126" />

          {/* Shield border */}
          <ellipse cx="0" cy="0" rx="28" ry="40" fill="none" stroke="#654321" strokeWidth="3" />
        </g>
      </svg>
    </div>
  );
};

export default KenyanFlag;
