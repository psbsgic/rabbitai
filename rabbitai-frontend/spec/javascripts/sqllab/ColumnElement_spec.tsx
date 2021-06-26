
import React from 'react';
import { styledMount as mount } from 'spec/helpers/theming';
import ColumnElement from 'src/SqlLab/components/ColumnElement';

import { mockedActions, table } from './fixtures';

describe('ColumnElement', () => {
  const mockedProps = {
    actions: mockedActions,
    column: table.columns[0],
  };
  it('is valid with props', () => {
    expect(React.isValidElement(<ColumnElement {...mockedProps} />)).toBe(true);
  });
  it('renders a proper primary key', () => {
    const wrapper = mount(<ColumnElement column={table.columns[0]} />);
    expect(wrapper.find('i.fa-key')).toExist();
    expect(wrapper.find('.col-name').first().text()).toBe('id');
  });
  it('renders a multi-key column', () => {
    const wrapper = mount(<ColumnElement column={table.columns[1]} />);
    expect(wrapper.find('i.fa-link')).toExist();
    expect(wrapper.find('i.fa-bookmark')).toExist();
    expect(wrapper.find('.col-name').first().text()).toBe('first_name');
  });
  it('renders a column with no keys', () => {
    const wrapper = mount(<ColumnElement column={table.columns[2]} />);
    expect(wrapper.find('i')).not.toExist();
    expect(wrapper.find('.col-name').first().text()).toBe('last_name');
  });
});
