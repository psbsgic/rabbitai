import memoizeOne from 'memoize-one';
import { getChartControlPanelRegistry } from '@superset-ui/core';
import {
  ControlPanelSectionConfig,
  expandControlConfig,
} from '@superset-ui/chart-controls';

/**
 * 从给定控制面板配置查找具有指定名称的控件。
 *
 * @param controlPanelSections 控制面板节。
 * @param controlKey 要查找控件的键（名称）。
 */
export function findControlItem(
  controlPanelSections: ControlPanelSectionConfig[],
  controlKey: string,
) {
  return (
    controlPanelSections
      .map(section => section.controlSetRows)
      .flat(2)
      .find(
        control =>
          controlKey === control ||
          (control !== null &&
            typeof control === 'object' &&
            'name' in control &&
            control.name === controlKey),
      ) ?? null
  );
}

/**
 * 获取缓存的控件配置。
 */
const getMemoizedControlConfig = memoizeOne(
  (controlKey, controlPanelConfig) => {
    const {
      controlOverrides = {},
      controlPanelSections = [],
    } = controlPanelConfig;
    const control = expandControlConfig(
      findControlItem(controlPanelSections, controlKey),
      controlOverrides,
    );
    return control && 'config' in control ? control.config : control;
  },
);

/**
 * 获取控件配置。
 *
 * @param controlKey 控件名称。
 * @param vizType 可视类型。
 */
export const getControlConfig = function getControlConfig(
  controlKey: string,
  vizType: string,
) {
  const controlPanelConfig = getChartControlPanelRegistry().get(vizType) || {};
  return getMemoizedControlConfig(controlKey, controlPanelConfig);
};
