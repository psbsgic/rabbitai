// Menu App. Used in views that do not already include the Menu component in the layout.
// eg, backend rendered views

import React from 'react';
import ReactDOM from 'react-dom';
import { CacheProvider } from '@emotion/react';
import createCache from '@emotion/cache';
import { ThemeProvider } from '@rabbitai-ui/core';
import Menu from 'src/components/Menu/Menu';
import { theme } from 'src/preamble';

const container = document.getElementById('app');
const bootstrapJson = container?.getAttribute('data-bootstrap') ?? '{}';
const bootstrap = JSON.parse(bootstrapJson);
const menu = { ...bootstrap.common.menu_data };

const emotionCache = createCache({
  key: 'menu',
});

const app = (
  // @ts-ignore: emotion types defs are incompatible between core and cache
  <CacheProvider value={emotionCache}>
    <ThemeProvider theme={theme}>
      <Menu data={menu} />
    </ThemeProvider>
  </CacheProvider>
);

ReactDOM.render(app, document.getElementById('app-menu'));
