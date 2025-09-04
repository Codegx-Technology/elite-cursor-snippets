// [SNIPPET]: surgicalfix + kenyafirst + thinkwithai + refactorclean
// [CONTEXT]: Tailwind CSS v4 configuration with Kenya-first design system
// [GOAL]: Fix Tailwind utilities not loading by using correct v4 configuration
// [TASK]: Create minimal, working Tailwind v4 config that loads utilities properly

import { colors, fontFamilies } from './src/config/designTokens';

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        ...colors, // Use imported colors
      },
      fontFamily: {
        ...fontFamilies, // Use imported font families
      },
      animation: {
        'float': 'float 3s ease-in-out infinite'
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' }
        }
      }
    },
  },
  plugins: [],
}
