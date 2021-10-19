import { getChartIdAndColumnFromFilterKey } from './getDashboardFilterKey';

// input: { [id_column1]: values, [id_column2]: values }
// output: { id: { column1: values, column2: values } }
export default function serializeActiveFilterValues(activeFilters) {
  return Object.entries(activeFilters).reduce((map, entry) => {
    const [filterKey, { values }] = entry;
    const { chartId, column } = getChartIdAndColumnFromFilterKey(filterKey);
    const entryByChartId = {
      ...map[chartId],
      [column]: values,
    };
    return {
      ...map,
      [chartId]: entryByChartId,
    };
  }, {});
}
