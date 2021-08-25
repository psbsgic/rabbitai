import { createStore, applyMiddleware, compose } from 'redux';
import thunk from 'redux-thunk';

import { rootReducer } from 'src/views/store';

import mockState from './mockState';
import {
  dashboardLayoutWithTabs,
  dashboardLayoutWithChartsInTabsAndRoot,
} from './mockDashboardLayout';
import { sliceId } from './mockChartQueries';
import { dashboardFilters } from './mockDashboardFilters';
import { nativeFilters, dataMaskWith2Filters } from './mockNativeFilters';

export const storeWithState = state =>
  createStore(rootReducer, state, compose(applyMiddleware(thunk)));

export const getMockStore = overrideState =>
  createStore(
    rootReducer,
    { ...mockState, ...overrideState },
    compose(applyMiddleware(thunk)),
  );

export const mockStore = getMockStore();

export const getMockStoreWithTabs = () =>
  createStore(
    rootReducer,
    {
      ...mockState,
      dashboardLayout: dashboardLayoutWithTabs,
      dashboardFilters: {},
    },
    compose(applyMiddleware(thunk)),
  );

export const getMockStoreWithChartsInTabsAndRoot = () =>
  createStore(
    rootReducer,
    {
      ...mockState,
      dashboardLayout: dashboardLayoutWithChartsInTabsAndRoot,
      dashboardFilters: {},
    },
    compose(applyMiddleware(thunk)),
  );

export const mockStoreWithTabs = getMockStoreWithTabs();
export const mockStoreWithChartsInTabsAndRoot = getMockStoreWithChartsInTabsAndRoot();

export const sliceIdWithAppliedFilter = sliceId + 1;
export const sliceIdWithRejectedFilter = sliceId + 2;

// has one chart with a filter that has been applied,
// one chart with a filter that has been rejected,
// and one chart with no filters set.
export const getMockStoreWithFilters = () =>
  createStore(rootReducer, {
    ...mockState,
    dashboardFilters,
    dataMask: dataMaskWith2Filters,
    charts: {
      ...mockState.charts,
      [sliceIdWithAppliedFilter]: {
        ...mockState.charts[sliceId],
        queryResponse: {
          status: 'success',
          applied_filters: [{ column: 'region' }],
          rejected_filters: [],
        },
      },
      [sliceIdWithRejectedFilter]: {
        ...mockState.charts[sliceId],
        queryResponse: {
          status: 'success',
          applied_filters: [],
          rejected_filters: [{ column: 'region', reason: 'not_in_datasource' }],
        },
      },
    },
  });

export const getMockStoreWithNativeFilters = () =>
  createStore(rootReducer, {
    ...mockState,
    nativeFilters,
    dataMask: dataMaskWith2Filters,
    charts: {
      ...mockState.charts,
      [sliceIdWithAppliedFilter]: {
        ...mockState.charts[sliceId],
        queryResponse: {
          status: 'success',
          applied_filters: [{ column: 'region' }],
          rejected_filters: [],
        },
      },
      [sliceIdWithRejectedFilter]: {
        ...mockState.charts[sliceId],
        queryResponse: {
          status: 'success',
          applied_filters: [],
          rejected_filters: [{ column: 'region', reason: 'not_in_datasource' }],
        },
      },
    },
  });

export const stateWithoutNativeFilters = {
  ...mockState,
  charts: {
    ...mockState.charts,
    [sliceIdWithAppliedFilter]: {
      ...mockState.charts[sliceId],
      queryResponse: {
        status: 'success',
        applied_filters: [{ column: 'region' }],
        rejected_filters: [],
      },
    },
    [sliceIdWithRejectedFilter]: {
      ...mockState.charts[sliceId],
      queryResponse: {
        status: 'success',
        applied_filters: [],
        rejected_filters: [{ column: 'region', reason: 'not_in_datasource' }],
      },
    },
  },
  dashboardInfo: {
    dash_edit_perm: true,
    metadata: {
      native_filter_configuration: [],
    },
  },
  dataMask: {},
  nativeFilters: { filters: {}, filterSets: {} },
};
