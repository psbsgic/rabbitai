
import { getChartIdAndColumnFromFilterKey } from './getDashboardFilterKey';

// input: { [id_column1]: values, [id_column2]: values }
// output: { column1: values, column2: values }
export default function getFilterValuesByFilterId({
  activeFilters = {},
  filterId,
}) {
  return Object.entries(activeFilters).reduce((map, entry) => {
    const [filterKey, { values }] = entry;
    const { chartId, column } = getChartIdAndColumnFromFilterKey(filterKey);
    if (chartId === filterId) {
      return {
        ...map,
        [column]: values,
      };
    }
    return map;
  }, {});
}
