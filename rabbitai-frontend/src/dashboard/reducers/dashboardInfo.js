import { DASHBOARD_INFO_UPDATED } from '../actions/dashboardInfo';
import { HYDRATE_DASHBOARD } from '../actions/hydrate';

export default function dashboardStateReducer(state = {}, action) {
  switch (action.type) {
    case DASHBOARD_INFO_UPDATED:
      return {
        ...state,
        ...action.newInfo,
        // server-side compare last_modified_time in second level
        last_modified_time: Math.round(new Date().getTime() / 1000),
      };
    case HYDRATE_DASHBOARD:
      return {
        ...state,
        ...action.data.dashboardInfo,
        // set async api call data
      };
    default:
      return state;
  }
}
