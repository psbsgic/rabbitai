import {
  buildQueryContext,
  GenericDataType,
  QueryObject,
  QueryObjectFilterClause,
} from '@superset-ui/core';
import { BuildQuery } from '@superset-ui/core/lib/chart/registries/ChartBuildQueryRegistrySingleton';
import { DEFAULT_FORM_DATA, PluginFilterSelectQueryFormData } from './types';

const buildQuery: BuildQuery<PluginFilterSelectQueryFormData> = (
  formData: PluginFilterSelectQueryFormData,
  options,
) => {
  const { search, coltypeMap } = options?.ownState || {};
  const { sortAscending, sortMetric } = { ...DEFAULT_FORM_DATA, ...formData };
  return buildQueryContext(formData, baseQueryObject => {
    const { columns = [], filters = [] } = baseQueryObject;
    const extraFilters: QueryObjectFilterClause[] = [];
    if (search) {
      columns.forEach(column => {
        if (coltypeMap[column] === GenericDataType.STRING) {
          extraFilters.push({
            col: column,
            op: 'ILIKE',
            val: `%${search}%`,
          });
        } else if (
          coltypeMap[column] === GenericDataType.NUMERIC &&
          !Number.isNaN(Number(search))
        ) {
          // for numeric columns we apply a >= where clause
          extraFilters.push({
            col: column,
            op: '>=',
            val: Number(search),
          });
        }
      });
    }

    const sortColumns = sortMetric ? [sortMetric] : columns;
    const query: QueryObject[] = [
      {
        ...baseQueryObject,
        groupby: columns,
        metrics: sortMetric ? [sortMetric] : [],
        filters: filters.concat(extraFilters),
        orderby:
          sortMetric || sortAscending !== undefined
            ? sortColumns.map(column => [column, !!sortAscending])
            : [],
      },
    ];
    return query;
  });
};

export default buildQuery;
