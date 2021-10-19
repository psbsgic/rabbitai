import { getChartControlPanelRegistry } from '@superset-ui/core';
import MainPreset from '../visualizations/presets/MainPreset';
import setupPluginsExtra from './setupPluginsExtra';

import Separator from '../explore/controlPanels/Separator';
import TimeTable from '../explore/controlPanels/TimeTable';

/**
 * 设置插件，建立插件注册表，注册相关插件：MainPreset、Separator、TimeTable等。
 */
export default function setupPlugins() {
  // 注册已定义的各种插件
  new MainPreset().register();

  // 注册Separator、TimeTable
  getChartControlPanelRegistry()
    .registerValue('separator', Separator)
    .registerValue('time_table', TimeTable);

  // 注册自定义插件
  setupPluginsExtra();
}
