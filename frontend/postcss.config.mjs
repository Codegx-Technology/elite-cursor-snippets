// [SNIPPET]: surgicalfix + thinkwithai + refactorclean
// [CONTEXT]: PostCSS configuration for Tailwind CSS v4 compatibility
// [GOAL]: Fix Tailwind utilities not loading by using correct PostCSS setup
// [TASK]: Configure PostCSS to properly process Tailwind v4 directives

const config = {
  plugins: {
    "@tailwindcss/postcss": {},
  },
};

export default config;
