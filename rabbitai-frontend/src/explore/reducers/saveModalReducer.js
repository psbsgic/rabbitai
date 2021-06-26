
/* eslint camelcase: 0 */
import * as actions from '../actions/saveModalActions';

export default function saveModalReducer(state = {}, action) {
  const actionHandlers = {
    [actions.FETCH_DASHBOARDS_SUCCEEDED]() {
      return { ...state, dashboards: action.choices };
    },
    [actions.FETCH_DASHBOARDS_FAILED]() {
      return {
        ...state,
        saveModalAlert: `fetching dashboards failed for ${action.userId}`,
      };
    },
    [actions.SAVE_SLICE_FAILED]() {
      return { ...state, saveModalAlert: 'Failed to save slice' };
    },
    [actions.SAVE_SLICE_SUCCESS](data) {
      return { ...state, data };
    },
    [actions.REMOVE_SAVE_MODAL_ALERT]() {
      return { ...state, saveModalAlert: null };
    },
  };

  if (action.type in actionHandlers) {
    return actionHandlers[action.type]();
  }
  return state;
}
