import type { StorybookConfig } from '@storybook/nextjs';

const config: StorybookConfig = {
  framework: '@storybook/nextjs',
  stories: ['../src/**/*.stories.@(js|jsx|ts|tsx)'],
  addons: [
    '@storybook/addon-essentials',
    '@storybook/addon-interactions',
    '@storybook/addon-a11y',
  ],
  docs: { autodocs: 'tag' },
  webpackFinal: async (config) => {
    // Workaround for SB_BUILDER-WEBPACK5_0002 cache shutdown hook error
    // Disable webpack cache for Storybook build (does not affect Next.js build)
    // See: builder-webpack5 issues on Windows/Next.js environments
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    (config as any).cache = false;
    return config;
  },
};

export default config;
