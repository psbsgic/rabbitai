
import { t } from '@rabbitai-ui/core';
import {
  ControlPanelConfig,
  sections,
  sharedControls,
} from '@rabbitai-ui/chart-controls';

const config: ControlPanelConfig = {
  controlPanelSections: [
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
              label: 'Column',
              description:
                'The numeric column based on which to calculate the range',
            },
          },
        ],
      ],
    },
  ],
};

export default config;
