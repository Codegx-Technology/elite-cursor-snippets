// frontend/src/config/designTokens.ts

/**
 * @file Design Tokens for Shujaa Studio UI.
 * @description Centralized source of truth for design values like colors, typography, and spacing.
 *              These tokens are also extended in tailwind.config.ts for consistent styling.
 */

export const colors = {
  kenya: {
    green: '#00A651',
    red: '#FF6B35',
    black: '#000000',
    white: '#FFFFFF'
  },
  cultural: {
    gold: '#FFD700',
    sunset: '#FF8C42',
    earth: '#8B4513',
    sky: '#87CEEB',
    savanna: '#F4A460'
  },
  // Add other core colors (primary, secondary, accent, etc.) here if they are not already defined
  // or if they need to be explicitly part of the design system.
};

export const fontFamilies = {
  sans: ['Inter', 'system-ui', 'sans-serif'],
  display: ['Poppins', 'Inter', 'sans-serif']
};

// You can add other design tokens here, e.g., spacing, breakpoints, border-radius, etc.
export const spacing = {
  'xs': '0.25rem',    // 4px
  'sm': '0.5rem',     // 8px
  'md': '1rem',       // 16px
  'lg': '1.5rem',     // 24px
  'xl': '2rem',       // 32px
  '2xl': '3rem',      // 48px
  '3xl': '4rem',      // 64px
};

export const breakpoints = {
  'sm': '640px',
  'md': '768px',
  'lg': '1024px',
  'xl': '1280px',
  '2xl': '1536px',
};

export const typography = {
  fontSizes: {
    'xs': '0.75rem',    // 12px
    'sm': '0.875rem',   // 14px
    'base': '1rem',     // 16px
    'lg': '1.125rem',   // 18px
    'xl': '1.25rem',    // 20px
    '2xl': '1.5rem',    // 24px
    '3xl': '1.875rem',  // 30px
    '4xl': '2.25rem',   // 36px
  },
  fontWeights: {
    'light': '300',
    'normal': '400',
    'medium': '500',
    'semibold': '600',
    'bold': '700',
    'extrabold': '800',
  },
  lineHeights: {
    'tight': '1.25',
    'snug': '1.375',
    'normal': '1.5',
    'relaxed': '1.625',
    'loose': '2',
  },
};

export const borderRadius = {
  'none': '0',
  'sm': '0.125rem',   // 2px
  'md': '0.375rem',   // 6px
  'lg': '0.5rem',     // 8px
  'xl': '0.75rem',    // 12px
  '2xl': '1rem',      // 16px
  '3xl': '1.5rem',    // 24px
  'full': '9999px',
};

export const shadows = {
  'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
  'md': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
  'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
  'xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
  'kenya': '0 8px 25px rgba(0, 166, 81, 0.15)', // Kenya green shadow
  'cultural': '0 8px 25px rgba(255, 215, 0, 0.2)', // Cultural gold shadow
};
