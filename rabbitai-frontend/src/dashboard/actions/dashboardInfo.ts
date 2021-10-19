import { Dispatch } from 'redux';
import { makeApi } from '@superset-ui/core';
import { ChartConfiguration, DashboardInfo } from '../reducers/types';

export const DASHBOARD_INFO_UPDATED = 'DASHBOARD_INFO_UPDATED';

// updates partially changed dashboard info
export function dashboardInfoChanged(newInfo: { metadata: any }) {
  return { type: DASHBOARD_INFO_UPDATED, newInfo };
}
export const SET_CHART_CONFIG_BEGIN = 'SET_CHART_CONFIG_BEGIN';
export interface SetChartConfigBegin {
  type: typeof SET_CHART_CONFIG_BEGIN;
  chartConfiguration: ChartConfiguration;
}
export const SET_CHART_CONFIG_COMPLETE = 'SET_CHART_CONFIG_COMPLETE';
export interface SetChartConfigComplete {
  type: typeof SET_CHART_CONFIG_COMPLETE;
  chartConfiguration: ChartConfiguration;
}
export const SET_CHART_CONFIG_FAIL = 'SET_CHART_CONFIG_FAIL';
export interface SetChartConfigFail {
  type: typeof SET_CHART_CONFIG_FAIL;
  chartConfiguration: ChartConfiguration;
}
export const setChartConfiguration = (
  chartConfiguration: ChartConfiguration,
) => async (dispatch: Dispatch, getState: () => any) => {
  dispatch({
    type: SET_CHART_CONFIG_BEGIN,
    chartConfiguration,
  });
  const { id, metadata } = getState().dashboardInfo;

  // TODO extract this out when makeApi supports url parameters
  const updateDashboard = makeApi<
    Partial<DashboardInfo>,
    { result: DashboardInfo }
  >({
    method: 'PUT',
    endpoint: `/api/v1/dashboard/${id}`,
  });

  try {
    const response = await updateDashboard({
      json_metadata: JSON.stringify({
        ...metadata,
        chart_configuration: chartConfiguration,
      }),
    });
    dispatch(
      dashboardInfoChanged({
        metadata: JSON.parse(response.result.json_metadata),
      }),
    );
    dispatch({
      type: SET_CHART_CONFIG_COMPLETE,
      chartConfiguration,
    });
  } catch (err) {
    dispatch({ type: SET_CHART_CONFIG_FAIL, chartConfiguration });
  }
};
