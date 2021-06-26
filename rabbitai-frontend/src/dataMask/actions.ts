
import { DataMask } from '@rabbitai-ui/core';
import { FilterConfiguration } from '../dashboard/components/nativeFilters/types';
import { FeatureFlag, isFeatureEnabled } from '../featureFlags';
import { Filters } from '../dashboard/reducers/types';

export const UPDATE_DATA_MASK = 'UPDATE_DATA_MASK';
export interface UpdateDataMask {
  type: typeof UPDATE_DATA_MASK;
  filterId: string;
  dataMask: DataMask;
}

export const SET_DATA_MASK_FOR_FILTER_CONFIG_COMPLETE =
  'SET_DATA_MASK_FOR_FILTER_CONFIG_COMPLETE';

export interface SetDataMaskForFilterConfigComplete {
  type: typeof SET_DATA_MASK_FOR_FILTER_CONFIG_COMPLETE;
  filterConfig: FilterConfiguration;
  filters?: Filters;
}

export const SET_DATA_MASK_FOR_FILTER_CONFIG_FAIL =
  'SET_DATA_MASK_FOR_FILTER_CONFIG_FAIL';

export interface SetDataMaskForFilterConfigFail {
  type: typeof SET_DATA_MASK_FOR_FILTER_CONFIG_FAIL;
  filterConfig: FilterConfiguration;
}
export function setDataMaskForFilterConfigComplete(
  filterConfig: FilterConfiguration,
  filters?: Filters,
): SetDataMaskForFilterConfigComplete {
  return {
    type: SET_DATA_MASK_FOR_FILTER_CONFIG_COMPLETE,
    filterConfig,
    filters,
  };
}
export function updateDataMask(
  filterId: string,
  dataMask: DataMask,
): UpdateDataMask {
  // Only apply data mask if one of the relevant features is enabled
  const isFeatureFlagActive =
    isFeatureEnabled(FeatureFlag.DASHBOARD_NATIVE_FILTERS) ||
    isFeatureEnabled(FeatureFlag.DASHBOARD_CROSS_FILTERS);
  return {
    type: UPDATE_DATA_MASK,
    filterId,
    dataMask: isFeatureFlagActive ? dataMask : {},
  };
}

export type AnyDataMaskAction =
  | UpdateDataMask
  | SetDataMaskForFilterConfigFail
  | SetDataMaskForFilterConfigComplete;
