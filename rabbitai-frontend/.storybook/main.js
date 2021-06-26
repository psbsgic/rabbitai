const path = require('path');

// webpack.config.js
const customConfig = require('../webpack.config.js');

module.exports = {
stories: ['../src/@(components|common|filters)/**/*.stories.@(t|j)sx'],
  addons: [
    '@storybook/addon-essentials',
    '@storybook/addon-links',
    '@storybook/preset-typescript',
    'storybook-addon-jsx',
    '@storybook/addon-knobs/register',
    'storybook-addon-paddings',
  ],
  webpackFinal: config => ({
    ...config,
    module: {
      ...config.module,
      rules: customConfig.module.rules,
    },
    resolve: {
      ...config.resolve,
      ...customConfig.resolve,
    },
    plugins: [...config.plugins, ...customConfig.plugins],
  }),
};
