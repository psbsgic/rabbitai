
import { SET_DATASOURCE } from '../actions/datasources';
import { HYDRATE_DASHBOARD } from '../actions/hydrate';

export default function datasourceReducer(datasources = {}, action) {
  const actionHandlers = {
    [HYDRATE_DASHBOARD]() {
      return action.data.datasources;
    },
    [SET_DATASOURCE]() {
      return action.datasource;
    },
  };

  if (action.type in actionHandlers) {
    if (action.key) {
      return {
        ...datasources,
        [action.key]: actionHandlers[action.type](
          datasources[action.key],
          action,
        ),
      };
    }
    return actionHandlers[action.type]();
  }
  return datasources;
}
