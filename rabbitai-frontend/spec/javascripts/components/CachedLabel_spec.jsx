import React from 'react';
import { shallow } from 'enzyme';

import Label from 'src/components/Label';
import CachedLabel from 'src/components/CachedLabel';

describe('CachedLabel', () => {
  const defaultProps = {
    onClick: () => {},
    cachedTimestamp: '2017-01-01',
  };

  it('is valid', () => {
    expect(React.isValidElement(<CachedLabel {...defaultProps} />)).toBe(true);
  });
  it('renders', () => {
    const wrapper = shallow(<CachedLabel {...defaultProps} />);
    expect(wrapper.find(Label)).toExist();
  });
});
