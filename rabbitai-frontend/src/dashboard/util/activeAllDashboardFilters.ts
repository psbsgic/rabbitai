import { DataMaskStateWithId } from 'src/dataMask/types';
import { JsonObject } from '@superset-ui/core';
import { CHART_TYPE } from './componentTypes';
import { Scope } from '../components/nativeFilters/types';
import { ActiveFilters, Layout, LayoutItem } from '../types';
import { ChartConfiguration, Filters } from '../reducers/types';
import { DASHBOARD_ROOT_ID } from './constants';

// Looking for affected chart scopes and values
export const findAffectedCharts = ({
  child,
  layout,
  scope,
  activeFilters,
  filterId,
  extraFormData,
}: {
  child: string;
  layout: { [key: string]: LayoutItem };
  scope: Scope;
  activeFilters: ActiveFilters;
  filterId: string;
  extraFormData: any;
}) => {
  const chartId = layout[child]?.meta?.chartId;
  if (layout[child].type === CHART_TYPE) {
    // Ignore excluded charts
    if (scope.excluded.includes(chartId)) {
      return;
    }
    if (!activeFilters[filterId]) {
      // Small mutation but simplify logic
      // eslint-disable-next-line no-param-reassign
      activeFilters[filterId] = {
        scope: [],
        values: extraFormData,
      };
    }
    // Add not excluded chart scopes(to know what charts refresh) and values(refresh only if its value changed)
    activeFilters[filterId].scope.push(chartId);
    return;
  }
  // If child is not chart, recursive iterate over its children
  layout[child].children.forEach((child: string) =>
    findAffectedCharts({
      child,
      layout,
      scope,
      activeFilters,
      filterId,
      extraFormData,
    }),
  );
};

export const getRelevantDataMask = (
  dataMask: DataMaskStateWithId,
  prop: string,
): JsonObject | DataMaskStateWithId =>
  Object.values(dataMask)
    .filter(item => item[prop])
    .reduce(
      (prev, next) => ({ ...prev, [next.id]: prop ? next[prop] : next }),
      {},
    );

export const getAllActiveFilters = ({
  chartConfiguration,
  nativeFilters,
  dataMask,
  layout,
}: {
  chartConfiguration: ChartConfiguration;
  dataMask: DataMaskStateWithId;
  nativeFilters: Filters;
  layout: Layout;
}): ActiveFilters => {
  const activeFilters = {};

  // Combine native filters with cross filters, because they have similar logic
  Object.values(dataMask).forEach(({ id: filterId, extraFormData }) => {
    const scope = nativeFilters?.[filterId]?.scope ??
      chartConfiguration?.[filterId]?.crossFilters?.scope ?? {
        rootPath: [DASHBOARD_ROOT_ID],
        excluded: [filterId],
      };
    // Iterate over all roots to find all affected charts
    scope.rootPath.forEach((layoutItemId: string | number) => {
      layout[layoutItemId]?.children?.forEach((child: string) => {
        // Need exclude from affected charts, charts that located in scope `excluded`
        findAffectedCharts({
          child,
          layout,
          scope,
          activeFilters,
          filterId,
          extraFormData,
        });
      });
    });
  });
  return activeFilters;
};
