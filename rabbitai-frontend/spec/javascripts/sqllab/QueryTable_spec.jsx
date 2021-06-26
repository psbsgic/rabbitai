
import React from 'react';
import thunk from 'redux-thunk';
import configureStore from 'redux-mock-store';
import { styledMount as mount } from 'spec/helpers/theming';
import QueryTable from 'src/SqlLab/components/QueryTable';
import TableView from 'src/components/TableView';
import { TableCollection } from 'src/components/dataViewCommon';
import { Provider } from 'react-redux';
import { queries, user } from './fixtures';

describe('QueryTable', () => {
  const mockedProps = {
    queries,
    displayLimit: 100,
  };
  it('is valid', () => {
    expect(React.isValidElement(<QueryTable displayLimit={100} />)).toBe(true);
  });
  it('is valid with props', () => {
    expect(React.isValidElement(<QueryTable {...mockedProps} />)).toBe(true);
  });
  it('renders a proper table', () => {
    const mockStore = configureStore([thunk]);
    const store = mockStore({
      sqlLab: user,
    });

    const wrapper = mount(
      <Provider store={store}>
        <QueryTable {...mockedProps} />
      </Provider>,
    );
    const tableWrapper = wrapper.find(TableView).find(TableCollection);

    expect(wrapper.find(TableView)).toExist();
    expect(tableWrapper.find('table')).toExist();
    expect(tableWrapper.find('table').find('thead').find('tr')).toHaveLength(1);
    expect(tableWrapper.find('table').find('tbody').find('tr')).toHaveLength(2);
  });
});
