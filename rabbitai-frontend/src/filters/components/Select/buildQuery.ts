
import {
  buildQueryContext,
  GenericDataType,
  QueryObject,
  QueryObjectFilterClause,
} from '@rabbitai-ui/core';
import { BuildQuery } from '@rabbitai-ui/core/lib/chart/registries/ChartBuildQueryRegistrySingleton';
import { DEFAULT_FORM_DATA, PluginFilterSelectQueryFormData } from './types';

const buildQuery: BuildQuery<PluginFilterSelectQueryFormData> = (
  formData: PluginFilterSelectQueryFormData,
  options,
) => {
  const { search, coltypeMap } = options?.ownState || {};
  const { sortAscending, sortMetric } = { ...DEFAULT_FORM_DATA, ...formData };
  return buildQueryContext(formData, baseQueryObject => {
    const { columns = [], filters = [] } = baseQueryObject;
    const extra_filters: QueryObjectFilterClause[] = columns.map(column => {
      if (search && coltypeMap[column] === GenericDataType.STRING) {
        return {
          col: column,
          op: 'ILIKE',
          val: `%${search}%`,
        };
      }
      if (
        search &&
        coltypeMap[column] === GenericDataType.NUMERIC &&
        !Number.isNaN(Number(search))
      ) {
        // for numeric columns we apply a >= where clause
        return {
          col: column,
          op: '>=',
          val: Number(search),
        };
      }
      // if no search is defined, make sure the col value is not null
      return { col: column, op: 'IS NOT NULL' };
    });

    const sortColumns = sortMetric ? [sortMetric] : columns;
    const query: QueryObject[] = [
      {
        ...baseQueryObject,
        apply_fetch_values_predicate: true,
        groupby: columns,
        metrics: sortMetric ? [sortMetric] : [],
        filters: filters.concat(extra_filters),
        orderby:
          sortMetric || sortAscending
            ? sortColumns.map(column => [column, sortAscending])
            : [],
      },
    ];
    return query;
  });
};

export default buildQuery;
