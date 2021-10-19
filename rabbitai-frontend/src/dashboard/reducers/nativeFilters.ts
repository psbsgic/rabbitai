import {
  AnyFilterAction,
  SAVE_FILTER_SETS,
  SET_FILTER_CONFIG_COMPLETE,
  SET_IN_SCOPE_STATUS_OF_FILTERS,
  SET_FILTER_SETS_CONFIG_COMPLETE,
  SET_FOCUSED_NATIVE_FILTER,
  UNSET_FOCUSED_NATIVE_FILTER,
} from 'src/dashboard/actions/nativeFilters';
import { FilterSet, NativeFiltersState } from './types';
import { FilterConfiguration } from '../components/nativeFilters/types';
import { HYDRATE_DASHBOARD } from '../actions/hydrate';

export function getInitialState({
  filterSetsConfig,
  filterConfig,
  state: prevState,
}: {
  filterSetsConfig?: FilterSet[];
  filterConfig?: FilterConfiguration;
  state?: NativeFiltersState;
}): NativeFiltersState {
  const state: Partial<NativeFiltersState> = {};

  const filters = {};
  if (filterConfig) {
    filterConfig.forEach(filter => {
      const { id } = filter;
      filters[id] = filter;
    });
    state.filters = filters;
  } else {
    state.filters = prevState?.filters ?? {};
  }

  if (filterSetsConfig) {
    const filterSets = {};
    filterSetsConfig.forEach(filtersSet => {
      const { id } = filtersSet;
      filterSets[id] = filtersSet;
    });
    state.filterSets = filterSets;
  } else {
    state.filterSets = prevState?.filterSets ?? {};
  }
  state.focusedFilterId = undefined;
  return state as NativeFiltersState;
}

export default function nativeFilterReducer(
  state: NativeFiltersState = {
    filters: {},
    filterSets: {},
  },
  action: AnyFilterAction,
) {
  const { filterSets } = state;
  switch (action.type) {
    case HYDRATE_DASHBOARD:
      return {
        filters: action.data.nativeFilters.filters,
        filterSets: action.data.nativeFilters.filterSets,
      };
    case SAVE_FILTER_SETS:
      return {
        ...state,
        filterSets: {
          ...filterSets,
          [action.filtersSetId]: {
            id: action.filtersSetId,
            name: action.name,
            dataMask: action.dataMask,
          },
        },
      };

    case SET_FILTER_CONFIG_COMPLETE:
    case SET_IN_SCOPE_STATUS_OF_FILTERS:
      return getInitialState({ filterConfig: action.filterConfig, state });

    case SET_FILTER_SETS_CONFIG_COMPLETE:
      return getInitialState({
        filterSetsConfig: action.filterSetsConfig,
        state,
      });

    case SET_FOCUSED_NATIVE_FILTER:
      return {
        ...state,
        focusedFilterId: action.id,
      };

    case UNSET_FOCUSED_NATIVE_FILTER:
      return {
        ...state,
        focusedFilterId: undefined,
      };
    // TODO handle SET_FILTER_CONFIG_FAIL action
    default:
      return state;
  }
}
