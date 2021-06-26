import React from 'react';
import { t } from '@rabbitai-ui/core';
import { sections } from '@rabbitai-ui/chart-controls';

export default {
  controlPanelSections: [
    sections.legacyTimeseriesTime,
    {
      label: t('Filters configuration'),
      expanded: true,
      controlSetRows: [
        [
          {
            name: 'filter_configs',
            config: {
              type: 'CollectionControl',
              label: 'Filters',
              description: t('Filter configuration for the filter box'),
              validators: [],
              controlName: 'FilterBoxItemControl',
              mapStateToProps: ({ datasource }) => ({ datasource }),
            },
          },
        ],
        [<hr />],
        [
          {
            name: 'date_filter',
            config: {
              type: 'CheckboxControl',
              label: t('Date filter'),
              default: true,
              description: t('Whether to include a time filter'),
            },
          },
          {
            name: 'instant_filtering',
            config: {
              type: 'CheckboxControl',
              label: t('Instant filtering'),
              renderTrigger: true,
              default: false,
              description: t(
                'Check to apply filters instantly as they change instead of displaying [Apply] button',
              ),
            },
          },
        ],
        [
          {
            name: 'show_sqla_time_granularity',
            config: {
              type: 'CheckboxControl',
              label: t('Show SQL granularity dropdown'),
              default: false,
              description: t('Check to include SQL granularity dropdown'),
            },
          },
          {
            name: 'show_sqla_time_column',
            config: {
              type: 'CheckboxControl',
              label: t('Show SQL time column'),
              default: false,
              description: t('Check to include time column dropdown'),
            },
          },
        ],
        [
          {
            name: 'show_druid_time_granularity',
            config: {
              type: 'CheckboxControl',
              label: t('Show Druid granularity dropdown'),
              default: false,
              description: t('Check to include Druid granularity dropdown'),
            },
          },
          {
            name: 'show_druid_time_origin',
            config: {
              type: 'CheckboxControl',
              label: t('Show Druid time origin'),
              default: false,
              description: t('Check to include time origin dropdown'),
            },
          },
        ],
        ['adhoc_filters'],
      ],
    },
  ],
  controlOverrides: {
    adhoc_filters: {
      label: t('Limit selector values'),
      description: t(
        'These filters apply to the values available in the dropdowns',
      ),
    },
  },
};
