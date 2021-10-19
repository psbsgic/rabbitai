import { DataMaskStateWithId } from 'src/dataMask/types';
import { areObjectsEqual } from 'src/reduxUtils';
import { FilterState } from '@superset-ui/core';
import { Filter } from '../types';

export enum TabIds {
  AllFilters = 'allFilters',
  FilterSets = 'filterSets',
}

export function mapParentFiltersToChildren(
  filters: Filter[],
): { [id: string]: Filter[] } {
  const cascadeChildren = {};
  filters.forEach(filter => {
    const [parentId] = filter.cascadeParentIds || [];
    if (parentId) {
      if (!cascadeChildren[parentId]) {
        cascadeChildren[parentId] = [];
      }
      cascadeChildren[parentId].push(filter);
    }
  });
  return cascadeChildren;
}

export const getOnlyExtraFormData = (data: DataMaskStateWithId) =>
  Object.values(data).reduce(
    (prev, next) => ({ ...prev, [next.id]: next.extraFormData }),
    {},
  );

export const checkIsMissingRequiredValue = (
  filter: Filter,
  filterState?: FilterState,
) => {
  const value = filterState?.value;
  // TODO: this property should be unhardcoded
  return (
    filter.controlValues.enableEmptyFilter &&
    (value === null || value === undefined)
  );
};

export const checkIsApplyDisabled = (
  dataMaskSelected: DataMaskStateWithId,
  dataMaskApplied: DataMaskStateWithId,
  filters: Filter[],
) => {
  const dataSelectedValues = Object.values(dataMaskSelected);
  const dataAppliedValues = Object.values(dataMaskApplied);

  return (
    areObjectsEqual(
      getOnlyExtraFormData(dataMaskSelected),
      getOnlyExtraFormData(dataMaskApplied),
      { ignoreUndefined: true },
    ) ||
    dataSelectedValues.length !== dataAppliedValues.length ||
    filters.some(filter =>
      checkIsMissingRequiredValue(
        filter,
        dataMaskSelected?.[filter?.id]?.filterState,
      ),
    )
  );
};
