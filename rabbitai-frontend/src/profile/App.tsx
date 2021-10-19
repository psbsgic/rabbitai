import React from 'react';
import { hot } from 'react-hot-loader/root';
import thunk from 'redux-thunk';
import { createStore, applyMiddleware, compose, combineReducers } from 'redux';
import { Provider } from 'react-redux';
import { ThemeProvider } from '@superset-ui/core';
import App from 'src/profile/components/App';
import messageToastReducer from 'src/messageToasts/reducers';
import { initEnhancer } from 'src/reduxUtils';
import setupApp from 'src/setup/setupApp';
import './main.less';
import { theme } from 'src/preamble';
import ToastPresenter from 'src/messageToasts/containers/ToastPresenter';

setupApp();

const profileViewContainer = document.getElementById('app');
const bootstrap = JSON.parse(
  profileViewContainer?.getAttribute('data-bootstrap') ?? '{}',
);

const store = createStore(
  combineReducers({
    messageToasts: messageToastReducer,
  }),
  {},
  compose(applyMiddleware(thunk), initEnhancer(false)),
);

const Application = () => (
  <Provider store={store}>
    <ThemeProvider theme={theme}>
      <App user={bootstrap.user} />
      <ToastPresenter />
    </ThemeProvider>
  </Provider>
);

export default hot(Application);
