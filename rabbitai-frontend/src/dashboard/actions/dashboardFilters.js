
/* eslint-disable camelcase */
// util function to make sure filter is a valid slice in current dashboard
function isValidFilter(getState, chartId) {
  return getState().dashboardState.sliceIds.includes(chartId);
}

export const ADD_FILTER = 'ADD_FILTER';
export function addFilter(chartId, component, form_data) {
  return (dispatch, getState) => {
    if (isValidFilter(getState, chartId)) {
      return dispatch({ type: ADD_FILTER, chartId, component, form_data });
    }
    return getState().dashboardFilters;
  };
}

export const REMOVE_FILTER = 'REMOVE_FILTER';
export function removeFilter(chartId) {
  return (dispatch, getState) => {
    if (isValidFilter(getState, chartId)) {
      return dispatch({ type: REMOVE_FILTER, chartId });
    }
    return getState().dashboardFilters;
  };
}

export const CHANGE_FILTER = 'CHANGE_FILTER';
export function changeFilter(chartId, newSelectedValues, merge) {
  return (dispatch, getState) => {
    if (isValidFilter(getState, chartId)) {
      const components = getState().dashboardLayout.present;
      return dispatch({
        type: CHANGE_FILTER,
        chartId,
        newSelectedValues,
        merge,
        components,
      });
    }
    return getState().dashboardFilters;
  };
}

export const UPDATE_DIRECT_PATH_TO_FILTER = 'UPDATE_DIRECT_PATH_TO_FILTER';
export function updateDirectPathToFilter(chartId, path) {
  return (dispatch, getState) => {
    if (isValidFilter(getState, chartId)) {
      return dispatch({ type: UPDATE_DIRECT_PATH_TO_FILTER, chartId, path });
    }
    return getState().dashboardFilters;
  };
}

export const UPDATE_LAYOUT_COMPONENTS = 'UPDATE_LAYOUT_COMPONENTS';
export function updateLayoutComponents(components) {
  return dispatch => {
    dispatch({ type: UPDATE_LAYOUT_COMPONENTS, components });
  };
}

export const UPDATE_DASHBOARD_FILTERS_SCOPE = 'UPDATE_DASHBOARD_FILTERS_SCOPE';
export function updateDashboardFiltersScope(scopes) {
  return dispatch => {
    dispatch({ type: UPDATE_DASHBOARD_FILTERS_SCOPE, scopes });
  };
}
