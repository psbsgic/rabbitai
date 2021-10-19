import { ControlPanelConfig } from '@superset-ui/chart-controls';
import { t } from '@superset-ui/core';

const config: ControlPanelConfig = {
  controlPanelSections: [
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
