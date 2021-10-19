import { useSelector } from 'react-redux';
import { NativeFiltersState } from 'src/dashboard/reducers/types';
import { DataMaskStateWithId } from 'src/dataMask/types';
import { ExtraFormData } from '@superset-ui/core';
import { mergeExtraFormData } from '../../utils';

// eslint-disable-next-line import/prefer-default-export
export function useCascadingFilters(
  id: string,
  dataMaskSelected?: DataMaskStateWithId,
): ExtraFormData {
  const { filters } = useSelector<any, NativeFiltersState>(
    state => state.nativeFilters,
  );
  const filter = filters[id];
  const cascadeParentIds: string[] = filter?.cascadeParentIds ?? [];
  let cascadedFilters = {};
  cascadeParentIds.forEach(parentId => {
    const parentState = dataMaskSelected?.[parentId];
    cascadedFilters = mergeExtraFormData(
      cascadedFilters,
      parentState?.extraFormData,
    );
  });
  return cascadedFilters;
}
