
import { getChartIdAndColumnFromFilterKey } from './getDashboardFilterKey';

export default function getSelectedChartIdForFilterScopeTree({
  activeFilterField,
  checkedFilterFields,
}) {
  // we don't apply filter on filter_box itself, so we will disable
  // checkbox in filter scope selector.
  // this function returns chart id based on current filter scope selector local state:
  // 1. if in single-edit mode, return the chart id for selected filter field.
  // 2. if in multi-edit mode, if all filter fields are from same chart id,
  // return the single chart id.
  // otherwise, there is no chart to disable.
  if (activeFilterField) {
    return getChartIdAndColumnFromFilterKey(activeFilterField).chartId;
  }

  if (checkedFilterFields.length) {
    const { chartId } = getChartIdAndColumnFromFilterKey(
      checkedFilterFields[0],
    );

    if (
      checkedFilterFields.some(
        filterKey =>
          getChartIdAndColumnFromFilterKey(filterKey).chartId !== chartId,
      )
    ) {
      return null;
    }
    return chartId;
  }

  return null;
}
