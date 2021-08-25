import React from 'react';
import { addDecorator } from '@storybook/react';
import { jsxDecorator } from 'storybook-addon-jsx';
import { addParameters } from '@storybook/react';
import { withPaddings } from 'storybook-addon-paddings';
import { supersetTheme, ThemeProvider } from '@rabbitai-ui/core';
import { combineReducers, createStore, applyMiddleware, compose } from 'redux';
import thunk from 'redux-thunk';
import { Provider } from 'react-redux';
import reducerIndex from 'spec/helpers/reducerIndex';

import 'src/theme.ts';
import './storybook.css';

/**
 * 创建并返回存储对象。
 *
 * @type {Store<unknown, Action>}
 */
const store = createStore(
  combineReducers(reducerIndex),
  {},
  compose(applyMiddleware(thunk)),
);

const themeDecorator = Story => (
  <ThemeProvider theme={supersetTheme}>{<Story />}</ThemeProvider>
);

const providerDecorator = Story => (
  <Provider store={store}>
    <Story />
  </Provider>
);

addDecorator(jsxDecorator);
addDecorator(themeDecorator);
addDecorator(providerDecorator);
addDecorator(withPaddings);

addParameters({
  paddings: [
    { name: 'None', value: '0px' },
    { name: 'Small', value: '16px' },
    { name: 'Medium', value: '32px', default: true },
    { name: 'Large', value: '64px' },
  ],
  options: {
    storySort: {
      method: 'alphabetical',
    },
  },
});
