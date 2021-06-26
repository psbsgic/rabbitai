
import React from 'react';
import { shallow } from 'enzyme';

import Label from 'src/components/Label';
import QueryStateLabel from 'src/SqlLab/components/QueryStateLabel';

describe('SavedQuery', () => {
  const mockedProps = {
    query: {
      state: 'running',
    },
  };
  it('is valid', () => {
    expect(React.isValidElement(<QueryStateLabel {...mockedProps} />)).toBe(
      true,
    );
  });
  it('has an Overlay and a Popover', () => {
    const wrapper = shallow(<QueryStateLabel {...mockedProps} />);
    expect(wrapper.find(Label)).toExist();
  });
});
