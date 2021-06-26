
import React from 'react';
import { shallow } from 'enzyme';

import WithPopoverMenu from 'src/dashboard/components/menu/WithPopoverMenu';

describe('WithPopoverMenu', () => {
  const props = {
    children: <div id="child" />,
    disableClick: false,
    menuItems: [<div id="menu1" />, <div id="menu2" />],
    onChangeFocus() {},
    shouldFocus: () => true, // needed for mock
    isFocused: false,
    editMode: false,
  };

  function setup(overrideProps) {
    const wrapper = shallow(<WithPopoverMenu {...props} {...overrideProps} />);
    return wrapper;
  }

  it('should render a div with class "with-popover-menu"', () => {
    const wrapper = setup();
    expect(wrapper.find('.with-popover-menu')).toExist();
  });

  it('should render the passed children', () => {
    const wrapper = setup();
    expect(wrapper.find('#child')).toExist();
  });

  it('should focus on click in editMode', () => {
    const wrapper = setup();
    expect(wrapper.state('isFocused')).toBe(false);

    wrapper.simulate('click');
    expect(wrapper.state('isFocused')).toBe(false);

    wrapper.setProps({ ...props, editMode: true });
    wrapper.simulate('click');
    expect(wrapper.state('isFocused')).toBe(true);
  });

  it('should render menuItems when focused', () => {
    const wrapper = setup({ editMode: true });
    expect(wrapper.find('#menu1')).not.toExist();
    expect(wrapper.find('#menu2')).not.toExist();

    wrapper.simulate('click');
    expect(wrapper.find('#menu1')).toExist();
    expect(wrapper.find('#menu2')).toExist();
  });

  it('should not focus when disableClick=true', () => {
    const wrapper = setup({ disableClick: true, editMode: true });
    expect(wrapper.state('isFocused')).toBe(false);

    wrapper.simulate('click');
    expect(wrapper.state('isFocused')).toBe(false);
  });

  it('should use the passed shouldFocus func to determine if it should focus', () => {
    const wrapper = setup({ editMode: true, shouldFocus: () => false });
    expect(wrapper.state('isFocused')).toBe(false);

    wrapper.simulate('click');
    expect(wrapper.state('isFocused')).toBe(false);
  });
});
