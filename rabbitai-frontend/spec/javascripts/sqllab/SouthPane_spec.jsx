import React from 'react';
import configureStore from 'redux-mock-store';
import thunk from 'redux-thunk';
import { styledShallow as shallow } from 'spec/helpers/theming';
import SouthPaneContainer from 'src/SqlLab/components/SouthPane/state';
import ResultSet from 'src/SqlLab/components/ResultSet';
import '@testing-library/jest-dom/extend-expect';
import { STATUS_OPTIONS } from 'src/SqlLab/constants';
import { initialState } from './fixtures';

const mockedProps = {
  editorQueries: [
    {
      cached: false,
      changedOn: Date.now(),
      db: 'main',
      dbId: 1,
      id: 'LCly_kkIN',
      startDttm: Date.now(),
    },
    {
      cached: false,
      changedOn: 1559238500401,
      db: 'main',
      dbId: 1,
      id: 'lXJa7F9_r',
      startDttm: 1559238500401,
    },
    {
      cached: false,
      changedOn: 1559238506925,
      db: 'main',
      dbId: 1,
      id: '2g2_iRFMl',
      startDttm: 1559238506925,
    },
    {
      cached: false,
      changedOn: 1559238516395,
      db: 'main',
      dbId: 1,
      id: 'erWdqEWPm',
      startDttm: 1559238516395,
    },
  ],
  latestQueryId: 'LCly_kkIN',
  dataPreviewQueries: [],
  actions: {},
  activeSouthPaneTab: '',
  height: 1,
  displayLimit: 1,
  databases: {},
  offline: false,
};

const middlewares = [thunk];
const mockStore = configureStore(middlewares);
const store = mockStore(initialState);

describe('SouthPane', () => {
  const getWrapper = () =>
    shallow(<SouthPaneContainer store={store} {...mockedProps} />).dive();

  let wrapper;

  it('should render offline when the state is offline', () => {
    wrapper = getWrapper().dive();
    wrapper.setProps({ offline: true });
    expect(wrapper.childAt(0).text()).toBe(STATUS_OPTIONS.offline);
  });

  it('should pass latest query down to ResultSet component', () => {
    wrapper = getWrapper().dive();
    expect(wrapper.find(ResultSet)).toExist();
    expect(wrapper.find(ResultSet).props().query.id).toEqual(
      mockedProps.latestQueryId,
    );
  });
});
