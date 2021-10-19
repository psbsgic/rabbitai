import React from 'react';
import { styledMount as mount } from 'spec/helpers/theming';
import Security from 'src/profile/components/Security';
import Label from 'src/components/Label';
import { user, userNoPerms } from './fixtures';

describe('Security', () => {
  const mockedProps = {
    user,
  };
  it('is valid', () => {
    expect(React.isValidElement(<Security {...mockedProps} />)).toBe(true);
  });
  it('renders 2 role labels', () => {
    const wrapper = mount(<Security {...mockedProps} />);
    expect(wrapper.find('.roles').find(Label)).toHaveLength(2);
  });
  it('renders 2 datasource labels', () => {
    const wrapper = mount(<Security {...mockedProps} />);
    expect(wrapper.find('.datasources').find(Label)).toHaveLength(2);
  });
  it('renders 3 database labels', () => {
    const wrapper = mount(<Security {...mockedProps} />);
    expect(wrapper.find('.databases').find(Label)).toHaveLength(3);
  });
  it('renders no permission label when empty', () => {
    const wrapper = mount(<Security user={userNoPerms} />);
    expect(wrapper.find('.datasources').find(Label)).not.toExist();
    expect(wrapper.find('.databases').find(Label)).not.toExist();
  });
});
