import React from 'react';
import { shallow } from 'enzyme';
import RecentActivity from 'src/profile/components/RecentActivity';
import TableLoader from 'src/components/TableLoader';

import { user } from './fixtures';

describe('RecentActivity', () => {
  const mockedProps = {
    user,
  };
  it('is valid', () => {
    expect(React.isValidElement(<RecentActivity {...mockedProps} />)).toBe(
      true,
    );
  });

  it('renders a TableLoader', () => {
    const wrapper = shallow(<RecentActivity {...mockedProps} />);
    expect(wrapper.find(TableLoader)).toExist();
  });
});
