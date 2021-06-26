import React from 'react';
import { shallow } from 'enzyme';

import CollectionTable from 'src/CRUD/CollectionTable';
import mockDatasource from 'spec/fixtures/mockDatasource';

const props = {
  collection: mockDatasource['7__table'].columns,
  tableColumns: ['column_name', 'type', 'groupby'],
};

describe('CollectionTable', () => {
  let wrapper;
  let el;

  beforeEach(() => {
    el = <CollectionTable {...props} />;
    wrapper = shallow(el);
  });

  it('is valid', () => {
    expect(React.isValidElement(el)).toBe(true);
  });

  it('renders a table', () => {
    const { length } = mockDatasource['7__table'].columns;
    expect(wrapper.find('table')).toExist();
    expect(wrapper.find('tbody tr.row')).toHaveLength(length);
  });
});
