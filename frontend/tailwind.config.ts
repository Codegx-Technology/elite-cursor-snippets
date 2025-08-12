import type { Config } from 'tailwindcss'

// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorclean
// [CONTEXT]: Enterprise-grade Tailwind configuration with Kenya-first design system
// [GOAL]: Create stunning, culturally authentic design system with professional aesthetics
// [TASK]: Define comprehensive color palette, typography, and component styles

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      // Kenya-First Color Palette
      colors: {
        // Primary Kenya Flag Colors
        kenya: {
          green: '#00A651',
          red: '#FF6B35', 
          black: '#000000',
          white: '#FFFFFF'
        },
        
        // Cultural Accent Colors
        cultural: {
          gold: '#FFD700',
          sunset: '#FF8C42',
          earth: '#8B4513',
          sky: '#87CEEB',
          savanna: '#F4A460'
        },
        
        // Professional Grays
        charcoal: {
          50: '#F7FAFC',
          100: '#EDF2F7',
          200: '#E2E8F0',
          300: '#CBD5E0',
          400: '#A0AEC0',
          500: '#718096',
          600: '#4A5568',
          700: '#2D3748',
          800: '#1A202C',
          900: '#171923'
        },
        
        // Enterprise Status Colors
        status: {
          success: '#00A651',
          warning: '#FFD700',
          error: '#FF6B35',
          info: '#3182CE'
        },
        
        // Background Gradients
        background: {
          primary: '#FFFFFF',
          secondary: '#F8F9FA',
          dark: '#1A202C'
        }
      },
      
      // Typography Scale
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        display: ['Poppins', 'Inter', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace']
      },
      
      fontSize: {
        'xs': ['0.75rem', { lineHeight: '1rem' }],
        'sm': ['0.875rem', { lineHeight: '1.25rem' }],
        'base': ['1rem', { lineHeight: '1.5rem' }],
        'lg': ['1.125rem', { lineHeight: '1.75rem' }],
        'xl': ['1.25rem', { lineHeight: '1.75rem' }],
        '2xl': ['1.5rem', { lineHeight: '2rem' }],
        '3xl': ['1.875rem', { lineHeight: '2.25rem' }],
        '4xl': ['2.25rem', { lineHeight: '2.5rem' }],
        '5xl': ['3rem', { lineHeight: '1' }],
        '6xl': ['3.75rem', { lineHeight: '1' }]
      },
      
      // Spacing Scale
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '128': '32rem'
      },
      
      // Border Radius
      borderRadius: {
        'xl': '1rem',
        '2xl': '1.5rem',
        '3xl': '2rem'
      },
      
      // Box Shadows
      boxShadow: {
        'kenya': '0 4px 14px 0 rgba(0, 166, 81, 0.15)',
        'cultural': '0 4px 14px 0 rgba(255, 215, 0, 0.15)',
        'enterprise': '0 10px 25px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
        'glow': '0 0 20px rgba(0, 166, 81, 0.3)',
        'inner-glow': 'inset 0 2px 4px 0 rgba(0, 166, 81, 0.1)'
      },
      
      // Gradients
      backgroundImage: {
        'kenya-flag': 'linear-gradient(135deg, #00A651 0%, #FF6B35 50%, #000000 100%)',
        'kenya-sunset': 'linear-gradient(135deg, #FFD700 0%, #FF8C42 100%)',
        'kenya-earth': 'linear-gradient(135deg, #8B4513 0%, #F4A460 100%)',
        'enterprise': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'cultural-warm': 'linear-gradient(135deg, #FF8C42 0%, #FFD700 100%)',
        'professional': 'linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)',
        'dark-professional': 'linear-gradient(135deg, #2D3748 0%, #1A202C 100%)'
      },
      
      // Animation
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'slide-down': 'slideDown 0.3s ease-out',
        'scale-in': 'scaleIn 0.2s ease-out',
        'pulse-kenya': 'pulseKenya 2s infinite',
        'float': 'float 3s ease-in-out infinite'
      },
      
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' }
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' }
        },
        slideDown: {
          '0%': { transform: 'translateY(-10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' }
        },
        scaleIn: {
          '0%': { transform: 'scale(0.95)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' }
        },
        pulseKenya: {
          '0%, 100%': { boxShadow: '0 0 0 0 rgba(0, 166, 81, 0.7)' },
          '70%': { boxShadow: '0 0 0 10px rgba(0, 166, 81, 0)' }
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' }
        }
      },
      
      // Backdrop Blur
      backdropBlur: {
        'xs': '2px',
        'sm': '4px',
        'md': '8px',
        'lg': '12px',
        'xl': '16px'
      }
    },
  },
  plugins: [
    // Custom plugin for Kenya-first utilities
    function({ addUtilities }: any) {
      const newUtilities = {
        '.text-gradient-kenya': {
          background: 'linear-gradient(135deg, #00A651 0%, #FF6B35 100%)',
          '-webkit-background-clip': 'text',
          '-webkit-text-fill-color': 'transparent',
          'background-clip': 'text'
        },
        '.text-gradient-cultural': {
          background: 'linear-gradient(135deg, #FFD700 0%, #FF8C42 100%)',
          '-webkit-background-clip': 'text',
          '-webkit-text-fill-color': 'transparent',
          'background-clip': 'text'
        },
        '.glass-effect': {
          background: 'rgba(255, 255, 255, 0.1)',
          'backdrop-filter': 'blur(10px)',
          border: '1px solid rgba(255, 255, 255, 0.2)'
        },
        '.glass-dark': {
          background: 'rgba(0, 0, 0, 0.1)',
          'backdrop-filter': 'blur(10px)',
          border: '1px solid rgba(255, 255, 255, 0.1)'
        },
        '.hover-lift': {
          transition: 'transform 0.2s ease-out, box-shadow 0.2s ease-out',
          '&:hover': {
            transform: 'translateY(-2px)',
            'box-shadow': '0 10px 25px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)'
          }
        },
        '.btn-kenya': {
          background: 'linear-gradient(135deg, #00A651 0%, #00C65A 100%)',
          color: 'white',
          padding: '0.75rem 1.5rem',
          'border-radius': '0.5rem',
          'font-weight': '600',
          transition: 'all 0.2s ease-out',
          '&:hover': {
            background: 'linear-gradient(135deg, #008A44 0%, #00A651 100%)',
            transform: 'translateY(-1px)',
            'box-shadow': '0 4px 14px 0 rgba(0, 166, 81, 0.3)'
          }
        },
        '.btn-cultural': {
          background: 'linear-gradient(135deg, #FFD700 0%, #FFA500 100%)',
          color: '#1A202C',
          padding: '0.75rem 1.5rem',
          'border-radius': '0.5rem',
          'font-weight': '600',
          transition: 'all 0.2s ease-out',
          '&:hover': {
            background: 'linear-gradient(135deg, #FFC700 0%, #FFD700 100%)',
            transform: 'translateY(-1px)',
            'box-shadow': '0 4px 14px 0 rgba(255, 215, 0, 0.3)'
          }
        }
      }
      
      addUtilities(newUtilities)
    }
  ],
}

export default config
