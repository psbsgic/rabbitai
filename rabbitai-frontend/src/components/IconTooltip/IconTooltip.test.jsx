
import React from 'react';
import { shallow } from 'enzyme';
import { Tooltip } from 'src/components/Tooltip';
import { IconTooltip } from 'src/components/IconTooltip';

describe('IconTooltip', () => {
  const mockedProps = {
    tooltip: 'This is a tooltip',
  };
  it('renders', () => {
    expect(React.isValidElement(<IconTooltip>TEST</IconTooltip>)).toBe(true);
  });
  it('renders with props', () => {
    expect(
      React.isValidElement(<IconTooltip {...mockedProps}>TEST</IconTooltip>),
    ).toBe(true);
  });
  it('renders a tooltip', () => {
    const wrapper = shallow(<IconTooltip {...mockedProps}>TEST</IconTooltip>);
    expect(wrapper.find(Tooltip)).toExist();
  });
});
