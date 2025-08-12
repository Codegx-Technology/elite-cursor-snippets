// [SNIPPET]: surgicalfix + kenyafirst + thinkwithai + refactorclean
// [CONTEXT]: Tailwind CSS v4 configuration with Kenya-first design system
// [GOAL]: Fix Tailwind utilities not loading by using correct v4 configuration
// [TASK]: Create minimal, working Tailwind v4 config that loads utilities properly

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      // Kenya-First Color Palette
      colors: {
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
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        display: ['Poppins', 'Inter', 'sans-serif']
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
