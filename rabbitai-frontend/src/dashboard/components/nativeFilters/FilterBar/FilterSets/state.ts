
import { useMemo } from 'react';
import { useFilterSets } from '../state';

// eslint-disable-next-line import/prefer-default-export
export const useFilterSetNameDuplicated = (
  filterSetName: string,
  ignoreName?: string,
) => {
  const filterSets = useFilterSets();
  const filterSetFilterValues = Object.values(filterSets);
  const isFilterSetNameDuplicated = useMemo(
    () => !!filterSetFilterValues.find(({ name }) => name === filterSetName),
    [filterSetFilterValues, filterSetName],
  );
  if (ignoreName === filterSetName) {
    return false;
  }
  return isFilterSetNameDuplicated;
};
