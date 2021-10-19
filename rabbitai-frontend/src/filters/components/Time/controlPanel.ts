import { ControlPanelConfig } from '@superset-ui/chart-controls';
import { t } from '@superset-ui/core';
import { sharedControls } from '@superset-ui/chart-controls/lib';

const config: ControlPanelConfig = {
  // For control input types, see: rabbitai-frontend/src/explore/components/controls/index.js
  controlPanelSections: [
    {
      label: t('Query'),
      expanded: true,
      controlSetRows: [
        [
          {
            name: 'groupby',
            config: {
              ...sharedControls.groupby,
              label: 'Column',
              required: true,
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
