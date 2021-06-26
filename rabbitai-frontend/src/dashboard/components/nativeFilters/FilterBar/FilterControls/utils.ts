
import { Filter } from '../../types';
import { CascadeFilter } from '../CascadeFilters/types';
import { mapParentFiltersToChildren } from '../utils';

// eslint-disable-next-line import/prefer-default-export
export function buildCascadeFiltersTree(filters: Filter[]): CascadeFilter[] {
  const cascadeChildren = mapParentFiltersToChildren(filters);

  const getCascadeFilter = (filter: Filter): CascadeFilter => {
    const children = cascadeChildren[filter.id] || [];
    return {
      ...filter,
      cascadeChildren: children.map(getCascadeFilter),
    };
  };

  return filters
    .filter(filter => !filter.cascadeParentIds?.length)
    .map(getCascadeFilter);
}
