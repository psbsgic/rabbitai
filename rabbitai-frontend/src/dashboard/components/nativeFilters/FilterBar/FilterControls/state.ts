
import { useSelector } from 'react-redux';
import { NativeFiltersState } from 'src/dashboard/reducers/types';
import { mergeExtraFormData } from '../../utils';
import { useNativeFiltersDataMask } from '../state';

// eslint-disable-next-line import/prefer-default-export
export function useCascadingFilters(id: string) {
  const { filters } = useSelector<any, NativeFiltersState>(
    state => state.nativeFilters,
  );
  const filter = filters[id];
  const cascadeParentIds: string[] = filter?.cascadeParentIds ?? [];
  let cascadedFilters = {};
  const nativeFiltersDataMask = useNativeFiltersDataMask();
  cascadeParentIds.forEach(parentId => {
    const parentState = nativeFiltersDataMask[parentId] || {};
    const { extraFormData: parentExtra = {} } = parentState;
    cascadedFilters = mergeExtraFormData(cascadedFilters, parentExtra);
  });
  return cascadedFilters;
}
