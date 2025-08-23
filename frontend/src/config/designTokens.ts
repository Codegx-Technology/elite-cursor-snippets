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
  // Example:
  // 'xs': '4px',
  // 'sm': '8px',
  // 'md': '16px',
  // 'lg': '24px',
  // 'xl': '32px',
};

export const breakpoints = {
  // Example:
  // 'sm': '640px',
  // 'md': '768px',
  // 'lg': '1024px',
  // 'xl': '1280px',
};