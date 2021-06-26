

import getInitialState from './getInitialState';

const apiData = {
  defaultDbId: 1,
  common: {
    conf: {
      DEFAULT_SQLLAB_LIMIT: 1,
    },
  },
  active_tab: null,
  tab_state_ids: [],
  databases: [],
  queries: [],
  requested_query: null,
  user: {
    userId: 1,
    username: 'some name',
  },
};
const apiDataWithTabState = {
  ...apiData,
  tab_state_ids: [{ id: 1 }],
  active_tab: { id: 1, table_schemas: [] },
};
describe('getInitialState', () => {
  it('should output the user that is passed in', () => {
    expect(getInitialState(apiData).sqlLab.user.userId).toEqual(1);
  });
  it('should return undefined instead of null for templateParams', () => {
    expect(
      getInitialState(apiDataWithTabState).sqlLab.queryEditors[0]
        .templateParams,
    ).toBeUndefined();
  });
});
