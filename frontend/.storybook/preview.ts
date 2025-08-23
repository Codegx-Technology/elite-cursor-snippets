import type { Preview } from '@storybook/react';

// Import global styles if present (Next.js app styles)
try {
  // This import will succeed only if the file exists in the repo
  // eslint-disable-next-line @typescript-eslint/ban-ts-comment
  // @ts-ignore
  require('../src/app/globals.css');
} catch {}

const preview: Preview = {
  parameters: {
    actions: { argTypesRegex: '^on[A-Z].*' },
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/,
      },
    },
    a11y: {
      element: '#storybook-root',
      manual: false,
    },
  },
};

export default preview;
