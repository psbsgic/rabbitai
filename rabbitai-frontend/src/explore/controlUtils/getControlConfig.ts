
import memoizeOne from 'memoize-one';
import { getChartControlPanelRegistry } from '@rabbitai-ui/core';
import {
  ControlPanelSectionConfig,
  expandControlConfig,
} from '@rabbitai-ui/chart-controls';

/**
 * Find control item from control panel config.
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

export const getControlConfig = function getControlConfig(
  controlKey: string,
  vizType: string,
) {
  const controlPanelConfig = getChartControlPanelRegistry().get(vizType) || {};
  return getMemoizedControlConfig(controlKey, controlPanelConfig);
};
