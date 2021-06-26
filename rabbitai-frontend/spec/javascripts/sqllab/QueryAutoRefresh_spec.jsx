
import React from 'react';
import { shallow } from 'enzyme';
import sinon from 'sinon';
import thunk from 'redux-thunk';
import configureStore from 'redux-mock-store';

import QueryAutoRefresh from 'src/SqlLab/components/QueryAutoRefresh';
import { initialState, runningQuery } from './fixtures';

describe('QueryAutoRefresh', () => {
  const middlewares = [thunk];
  const mockStore = configureStore(middlewares);
  const sqlLab = {
    ...initialState.sqlLab,
    queries: {
      ryhMUZCGb: runningQuery,
    },
  };
  const state = {
    ...initialState,
    sqlLab,
  };
  const store = mockStore(state);
  const getWrapper = () =>
    shallow(<QueryAutoRefresh store={store} />)
      .dive()
      .dive();
  let wrapper;

  it('shouldCheckForQueries', () => {
    wrapper = getWrapper();
    expect(wrapper.instance().shouldCheckForQueries()).toBe(true);
  });

  it('setUserOffline', () => {
    wrapper = getWrapper();
    const spy = sinon.spy(wrapper.instance().props.actions, 'setUserOffline');

    // state not changed
    wrapper.setState({
      offline: false,
    });
    expect(spy.called).toBe(false);

    // state is changed
    wrapper.setState({
      offline: true,
    });
    expect(spy.callCount).toBe(1);
  });
});
