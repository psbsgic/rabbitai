import React, { Suspense } from 'react';
import { hot } from 'react-hot-loader/root';
import { Provider as ReduxProvider } from 'react-redux';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import { DndProvider } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';
import { QueryParamProvider } from 'use-query-params';
import { initFeatureFlags } from 'src/featureFlags';
import { ThemeProvider } from '@superset-ui/core';

import { DynamicPluginProvider } from 'src/components/DynamicPlugins';
import ErrorBoundary from 'src/components/ErrorBoundary';
import Loading from 'src/components/Loading';
import Menu from 'src/components/Menu/Menu';
import FlashProvider from 'src/components/FlashProvider';
import { theme } from 'src/preamble';
import ToastPresenter from 'src/messageToasts/containers/ToastPresenter';
import setupPlugins from 'src/setup/setupPlugins';
import setupApp from 'src/setup/setupApp';
import { routes, isFrontendRoute } from 'src/views/routes';
import { store } from './store';

setupApp();
setupPlugins();

const container = document.getElementById('app');
const bootstrap = JSON.parse(container?.getAttribute('data-bootstrap') ?? '{}');
const user = { ...bootstrap.user };
const menu = { ...bootstrap.common.menu_data };
const common = { ...bootstrap.common };
initFeatureFlags(bootstrap.common.feature_flags);

/**
 * 根上下文提供者，依次由ThemeProvider、ReduxProvider、DndProvider、
 * FlashProvider、DynamicPluginProvider、QueryParamProvider、{children}组成。
 *
 * @param children
 * @constructor
 */
const RootContextProviders: React.FC = ({ children }) => (
  <ThemeProvider theme={theme}>
    <ReduxProvider store={store}>
      <DndProvider backend={HTML5Backend}>
        <FlashProvider messages={common.flash_messages}>
          <DynamicPluginProvider>
            <QueryParamProvider
              ReactRouterRoute={Route}
              stringifyOptions={{ encode: false }}
            >
              {children}
            </QueryParamProvider>
          </DynamicPluginProvider>
        </FlashProvider>
      </DndProvider>
    </ReduxProvider>
  </ThemeProvider>
);

/**
 * 应用程序组件，Router、RootContextProviders、Menu、Switch、ToastPresenter。
 *
 * @constructor
 */
const App = () => (
  <Router>
    <RootContextProviders>
      <Menu data={menu} isFrontendRoute={isFrontendRoute} />
      <Switch>
        {routes.map(({ path, Component, props = {}, Fallback = Loading }) => (
          <Route path={path} key={path}>
            <Suspense fallback={<Fallback />}>
              <ErrorBoundary>
                <Component user={user} {...props} />
              </ErrorBoundary>
            </Suspense>
          </Route>
        ))}
      </Switch>
      <ToastPresenter />
    </RootContextProviders>
  </Router>
);

export default hot(App);
