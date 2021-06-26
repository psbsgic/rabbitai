import React from 'react';
import { hot } from 'react-hot-loader/root';
import { ThemeProvider } from '@rabbitai-ui/core';
import setupApp from '../setup/setupApp';
import setupPlugins from '../setup/setupPlugins';
import { DynamicPluginProvider } from '../components/DynamicPlugins';
import AddSliceContainer from './AddSliceContainer';
import { initFeatureFlags } from '../featureFlags';
import { theme } from '../preamble';

setupApp();
setupPlugins();

const addSliceContainer = document.getElementById('app');
const bootstrapData = JSON.parse(
  addSliceContainer?.getAttribute('data-bootstrap') || '{}',
);

initFeatureFlags(bootstrapData.common.feature_flags);

const App = () => (
  <ThemeProvider theme={theme}>
    <DynamicPluginProvider>
      <AddSliceContainer datasources={bootstrapData.datasources} />
    </DynamicPluginProvider>
  </ThemeProvider>
);

export default hot(App);
