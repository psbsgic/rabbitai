import { ControlPanelConfig, sections } from '@superset-ui/chart-controls';
import { t } from '@superset-ui/core';
import { sharedControls } from '@superset-ui/chart-controls/lib';
import { DEFAULT_FORM_DATA } from './types';

const { multiSelect } = DEFAULT_FORM_DATA;

const config: ControlPanelConfig = {
  controlPanelSections: [
    // @ts-ignore
    sections.legacyRegularTime,
    {
      label: t('Query'),
      expanded: true,
      controlSetRows: [
        [
          {
            name: 'groupby',
            config: {
              ...sharedControls.groupby,
              label: 'Columns to show',
              multiple: true,
              required: false,
            },
          },
        ],
      ],
    },
    {
      label: t('UI Configuration'),
      expanded: true,
      controlSetRows: [
        [
          {
            name: 'multiSelect',
            config: {
              type: 'CheckboxControl',
              label: t('Multiple select'),
              default: multiSelect,
              affectsDataMask: true,
              resetConfig: true,
              renderTrigger: true,
              description: t('Allow selecting multiple values'),
            },
          },
        ],
        [
          {
            name: 'enableEmptyFilter',
            config: {
              type: 'CheckboxControl',
              label: t('Required'),
              default: false,
              renderTrigger: true,
              description: t('User must select a value for this filter.'),
            },
          },
        ],
      ],
    },
  ],
};

export default config;
