import React from 'react';
import { hot } from 'react-hot-loader/root';
import { Provider } from 'react-redux';
import { DndProvider } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';
import { ThemeProvider } from '@superset-ui/core';
import { DynamicPluginProvider } from 'src/components/DynamicPlugins';
import ToastPresenter from '../messageToasts/containers/ToastPresenter';
import ExploreViewContainer from './components/ExploreViewContainer';
import setupApp from '../setup/setupApp';
import setupPlugins from '../setup/setupPlugins';
import './main.less';
import '../../stylesheets/reactable-pagination.less';
import { theme } from '../preamble';

setupApp();
setupPlugins();

const App = ({ store }) => (
  <Provider store={store}>
    <DndProvider backend={HTML5Backend}>
      <ThemeProvider theme={theme}>
        <DynamicPluginProvider>
          <ExploreViewContainer />
          <ToastPresenter />
        </DynamicPluginProvider>
      </ThemeProvider>
    </DndProvider>
  </Provider>
);

export default hot(App);
