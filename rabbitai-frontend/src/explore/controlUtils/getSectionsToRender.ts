import memoizeOne from 'memoize-one';
import {
  DatasourceType,
  getChartControlPanelRegistry,
} from '@superset-ui/core';
import {
  ControlPanelConfig,
  expandControlConfig,
} from '@superset-ui/chart-controls';

import * as SECTIONS from 'src/explore/controlPanels/sections';

const getMemoizedSectionsToRender = memoizeOne(
  (datasourceType: DatasourceType, controlPanelConfig: ControlPanelConfig) => {
    const {
      sectionOverrides = {},
      controlOverrides,
      controlPanelSections = [],
    } = controlPanelConfig;

    // default control panel sections
    const sections = { ...SECTIONS };

    // apply section overrides
    Object.entries(sectionOverrides).forEach(([section, overrides]) => {
      if (typeof overrides === 'object' && overrides.constructor === Object) {
        sections[section] = {
          ...sections[section],
          ...overrides,
        };
      } else {
        sections[section] = overrides;
      }
    });

    const { datasourceAndVizType } = sections;

    // list of datasource-specific controls that should be removed
    const invalidControls =
      datasourceType === 'table'
        ? ['granularity', 'druid_time_origin']
        : ['granularity_sqla', 'time_grain_sqla'];

    return [datasourceAndVizType]
      .concat(controlPanelSections)
      .filter(section => !!section)
      .map(section => {
        const { controlSetRows } = section;
        return {
          ...section,
          controlSetRows:
            controlSetRows?.map(row =>
              row
                .filter(
                  control =>
                    typeof control !== 'string' ||
                    !invalidControls.includes(control),
                )
                .map(item => expandControlConfig(item, controlOverrides)),
            ) || [],
        };
      });
  },
);

/**
 * Get the clean and processed control panel sections
 */
export function getSectionsToRender(
  vizType: string,
  datasourceType: DatasourceType,
) {
  const controlPanelConfig =
    // TODO: update `chartControlPanelRegistry` type to use ControlPanelConfig
    (getChartControlPanelRegistry().get(vizType) as ControlPanelConfig) || {};
  return getMemoizedSectionsToRender(datasourceType, controlPanelConfig);
}
