import { useEffect } from 'react';
import { findLastIndex } from 'lodash';
import { FilterRemoval } from './types';
import { usePrevious } from '../../../../common/hooks/usePrevious';

export const useRemoveCurrentFilter = (
  removedFilters: Record<string, FilterRemoval>,
  currentFilterId: string,
  filterIds: string[],
  setCurrentFilterId: Function,
) => {
  useEffect(() => {
    // if the currently viewed filter is fully removed, change to another tab
    const currentFilterRemoved = removedFilters[currentFilterId];
    if (currentFilterRemoved && !currentFilterRemoved.isPending) {
      const nextFilterIndex = findLastIndex(
        filterIds,
        id => !removedFilters[id] && id !== currentFilterId,
      );
      if (nextFilterIndex !== -1)
        setCurrentFilterId(filterIds[nextFilterIndex]);
    }
  }, [currentFilterId, removedFilters, filterIds]);
};

export const useOpenModal = (
  isOpen: boolean,
  addFilter: Function,
  createNewOnOpen?: boolean,
) => {
  const wasOpen = usePrevious(isOpen);
  // if this is a "create" modal rather than an "edit" modal,
  // add a filter on modal open
  useEffect(() => {
    if (createNewOnOpen && isOpen && !wasOpen) {
      addFilter();
    }
  }, [createNewOnOpen, isOpen, wasOpen, addFilter]);
};
