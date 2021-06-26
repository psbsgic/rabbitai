
import { getChartControlPanelRegistry } from '@rabbitai-ui/core';
import MainPreset from '../visualizations/presets/MainPreset';
import setupPluginsExtra from './setupPluginsExtra';

import Separator from '../explore/controlPanels/Separator';
import TimeTable from '../explore/controlPanels/TimeTable';

export default function setupPlugins() {
  new MainPreset().register();

  // TODO: Remove these shims once the control panel configs are moved into the plugin package.
  getChartControlPanelRegistry()
    .registerValue('separator', Separator)
    .registerValue('time_table', TimeTable);

  setupPluginsExtra();
}
