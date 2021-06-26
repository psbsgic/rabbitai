
import { t } from '@rabbitai-ui/core';

import { getDashboardFilterKey } from './getDashboardFilterKey';
import { ALL_FILTERS_ROOT } from './constants';
import { DASHBOARD_ROOT_TYPE } from './componentTypes';

export default function getFilterFieldNodesTree({ dashboardFilters = {} }) {
  const allFilters = Object.values(dashboardFilters).map(dashboardFilter => {
    const { chartId, filterName, columns, labels } = dashboardFilter;
    const children = Object.keys(columns).map(column => ({
      value: getDashboardFilterKey({ chartId, column }),
      label: labels[column] || column,
    }));
    return {
      value: chartId,
      label: filterName,
      children,
      showCheckbox: true,
    };
  });

  return [
    {
      value: ALL_FILTERS_ROOT,
      type: DASHBOARD_ROOT_TYPE,
      label: t('All filters'),
      children: allFilters,
    },
  ];
}
