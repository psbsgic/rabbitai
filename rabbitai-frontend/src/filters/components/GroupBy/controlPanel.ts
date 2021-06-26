
import { ControlPanelConfig, sections } from '@rabbitai-ui/chart-controls';
import { t } from '@rabbitai-ui/core';
import { DEFAULT_FORM_DATA } from './types';

const { multiSelect } = DEFAULT_FORM_DATA;

const config: ControlPanelConfig = {
  controlPanelSections: [
    // @ts-ignore
    sections.legacyRegularTime,
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
      ],
    },
  ],
};

export default config;
