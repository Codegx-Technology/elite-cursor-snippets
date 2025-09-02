import React from 'react';

interface KenyanFlagProps {
  size?: 'sm' | 'md' | 'lg' | 'xl';
  className?: string;
}

const KenyanFlag: React.FC<KenyanFlagProps> = ({ size = 'md', className = '' }) => {
  const sizeClasses = {
    sm: 'w-8 h-6',
    md: 'w-12 h-9',
    lg: 'w-16 h-12',
    xl: 'w-24 h-18'
  };

  return (
    <div className={`${sizeClasses[size]} ${className} inline-block`}>
      <svg
        viewBox="0 0 300 200"
        className="w-full h-full"
        xmlns="http://www.w3.org/2000/svg"
      >
        {/* Black stripe */}
        <rect x="0" y="0" width="300" height="40" fill="#000000" />
        
        {/* Red stripe */}
        <rect x="0" y="40" width="300" height="40" fill="#CE1126" />
        
        {/* Green stripe */}
        <rect x="0" y="80" width="300" height="40" fill="#007A3D" />
        
        {/* White stripes (separators) */}
        <rect x="0" y="35" width="300" height="10" fill="#FFFFFF" />
        <rect x="0" y="75" width="300" height="10" fill="#FFFFFF" />
        <rect x="0" y="115" width="300" height="10" fill="#FFFFFF" />
        
        {/* Green stripe */}
        <rect x="0" y="120" width="300" height="40" fill="#007A3D" />
        
        {/* Red stripe */}
        <rect x="0" y="160" width="300" height="40" fill="#CE1126" />
        
        {/* Black stripe */}
        <rect x="0" y="200" width="300" height="40" fill="#000000" />
        
        {/* Traditional Maasai Shield and Spears */}
        <g transform="translate(150, 100)">
          {/* Shield background */}
          <ellipse cx="0" cy="0" rx="25" ry="35" fill="#8B4513" stroke="#654321" strokeWidth="2" />
          
          {/* Shield pattern - traditional geometric design */}
          <path d="M-20,-25 L20,-25 L15,-15 L-15,-15 Z" fill="#FFFFFF" />
          <path d="M-15,-15 L15,-15 L10,-5 L-10,-5 Z" fill="#CE1126" />
          <path d="M-10,-5 L10,-5 L8,5 L-8,5 Z" fill="#000000" />
          <path d="M-8,5 L8,5 L6,15 L-6,15 Z" fill="#FFFFFF" />
          <path d="M-6,15 L6,15 L4,25 L-4,25 Z" fill="#CE1126" />
          
          {/* Spears - crossed behind shield */}
          <g>
            {/* Left spear */}
            <line x1="-35" y1="-45" x2="-15" y2="45" stroke="#8B4513" strokeWidth="3" />
            <polygon points="-37,-50 -33,-50 -35,-40" fill="#C0C0C0" />
            
            {/* Right spear */}
            <line x1="35" y1="-45" x2="15" y2="45" stroke="#8B4513" strokeWidth="3" />
            <polygon points="37,-50 33,-50 35,-40" fill="#C0C0C0" />
          </g>
          
          {/* Shield rim */}
          <ellipse cx="0" cy="0" rx="25" ry="35" fill="none" stroke="#654321" strokeWidth="3" />
        </g>
      </svg>
    </div>
  );
};

export default KenyanFlag;
