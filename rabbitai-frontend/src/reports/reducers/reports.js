/* eslint-disable camelcase */
import { SET_REPORT, ADD_REPORT, EDIT_REPORT } from '../actions/reports';

export default function reportsReducer(state = {}, action) {
  const actionHandlers = {
    [SET_REPORT]() {
      return {
        ...action.report.result.reduce(
          (obj, report) => ({ ...obj, [report.id]: report }),
          {},
        ),
      };
    },
    [ADD_REPORT]() {
      const report = action.json.result;
      report.id = action.json.id;
      return {
        ...state,
        [action.json.id]: report,
      };
    },
    [EDIT_REPORT]() {
      const report = action.json.result;
      report.id = action.json.id;
      return {
        ...state,
        [action.json.id]: report,
      };
    },
  };

  if (action.type in actionHandlers) {
    return actionHandlers[action.type]();
  }
  return state;
}
