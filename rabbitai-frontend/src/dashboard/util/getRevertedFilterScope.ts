import { getChartIdAndColumnFromFilterKey } from './getDashboardFilterKey';

interface FilterScopeMap {
  [key: string]: number[];
}

interface GetRevertFilterScopeProps {
  checked: string[];
  filterFields: string[];
  filterScopeMap: FilterScopeMap;
}

export default function getRevertedFilterScope({
  checked = [],
  filterFields = [],
  filterScopeMap = {},
}: GetRevertFilterScopeProps) {
  const checkedChartIdsByFilterField = checked.reduce<FilterScopeMap>(
    (map, value) => {
      const [chartId, filterField] = value.split(':');
      return {
        ...map,
        [filterField]: (map[filterField] || []).concat(parseInt(chartId, 10)),
      };
    },
    {},
  );

  return filterFields.reduce<FilterScopeMap>((map, filterField) => {
    const { chartId } = getChartIdAndColumnFromFilterKey(filterField);
    // force display filter_box chart as unchecked, but show checkbox as disabled
    const updatedCheckedIds = (
      checkedChartIdsByFilterField[filterField] || []
    ).filter(id => id !== chartId);

    return {
      ...map,
      [filterField]: {
        ...filterScopeMap[filterField],
        checked: updatedCheckedIds,
      },
    };
  }, {});
}
