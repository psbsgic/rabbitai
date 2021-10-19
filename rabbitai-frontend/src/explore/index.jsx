import React from 'react';
import ReactDOM from 'react-dom';
import { createStore, applyMiddleware, compose } from 'redux';
import thunk from 'redux-thunk';
import logger from '../middleware/loggerMiddleware';
import { initFeatureFlags } from '../featureFlags';
import { initEnhancer } from '../reduxUtils';
import getInitialState from './reducers/getInitialState';
import rootReducer from './reducers/index';
import App from './App';

const exploreViewContainer = document.getElementById('app');
const bootstrapData = JSON.parse(
  exploreViewContainer.getAttribute('data-bootstrap'),
);
initFeatureFlags(bootstrapData.common.feature_flags);
const initState = getInitialState(bootstrapData);
const store = createStore(
  rootReducer,
  initState,
  compose(applyMiddleware(thunk, logger), initEnhancer(false)),
);

ReactDOM.render(<App store={store} />, document.getElementById('app'));
