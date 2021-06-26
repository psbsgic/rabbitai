
import getFilterScopeNodesTree from './getFilterScopeNodesTree';
import getFilterScopeParentNodes from './getFilterScopeParentNodes';
import getKeyForFilterScopeTree from './getKeyForFilterScopeTree';
import getSelectedChartIdForFilterScopeTree from './getSelectedChartIdForFilterScopeTree';

export default function buildFilterScopeTreeEntry({
  checkedFilterFields = [],
  activeFilterField,
  filterScopeMap = {},
  layout = {},
}) {
  const key = getKeyForFilterScopeTree({
    checkedFilterFields,
    activeFilterField,
  });
  const editingList = activeFilterField
    ? [activeFilterField]
    : checkedFilterFields;
  const selectedChartId = getSelectedChartIdForFilterScopeTree({
    checkedFilterFields,
    activeFilterField,
  });
  const nodes = getFilterScopeNodesTree({
    components: layout,
    filterFields: editingList,
    selectedChartId,
  });
  const checkedChartIdSet = new Set();
  editingList.forEach(filterField => {
    (filterScopeMap[filterField].checked || []).forEach(chartId => {
      checkedChartIdSet.add(`${chartId}:${filterField}`);
    });
  });
  const checked = [...checkedChartIdSet];
  const expanded = filterScopeMap[key]
    ? filterScopeMap[key].expanded
    : getFilterScopeParentNodes(nodes, 1);

  return {
    [key]: {
      nodes,
      nodesFiltered: [...nodes],
      checked,
      expanded,
    },
  };
}
