

import { DataMaskStateWithId } from 'src/dataMask/types';
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
