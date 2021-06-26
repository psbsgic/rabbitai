
import React from 'react';
import { shallow } from 'enzyme';

import Label from 'src/components/Label';
import { Tooltip } from 'src/components/Tooltip';
import RowCountLabel from 'src/explore/components/RowCountLabel';

describe('RowCountLabel', () => {
  const defaultProps = {
    rowcount: 51,
    limit: 100,
  };

  it('is valid', () => {
    expect(React.isValidElement(<RowCountLabel {...defaultProps} />)).toBe(
      true,
    );
  });
  it('renders a Label and a Tooltip', () => {
    const wrapper = shallow(<RowCountLabel {...defaultProps} />);
    expect(wrapper.find(Label)).toExist();
    expect(wrapper.find(Tooltip)).toExist();
  });
  it('renders a danger when limit is reached', () => {
    const props = {
      rowcount: 100,
      limit: 100,
    };
    const wrapper = shallow(<RowCountLabel {...props} />);
    expect(wrapper.find(Label).first().props().type).toBe('danger');
  });
});
