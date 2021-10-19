import React from 'react';
import { ReactWrapper } from 'enzyme';
import {
  styledMount as mount,
  styledShallow as shallow,
} from 'spec/helpers/theming';

import Checkbox, {
  CheckboxChecked,
  CheckboxUnchecked,
} from 'src/components/Checkbox';

describe('Checkbox', () => {
  let wrapper: ReactWrapper;

  it('renders the base component', () => {
    expect(
      React.isValidElement(
        <Checkbox style={{}} checked={false} onChange={() => true} />,
      ),
    ).toBe(true);
  });

  describe('when unchecked', () => {
    it('renders the unchecked component', () => {
      const shallowWrapper = shallow(
        <Checkbox style={{}} checked={false} onChange={() => true} />,
      );
      expect(shallowWrapper.dive().find(CheckboxUnchecked)).toExist();
    });
  });

  describe('when checked', () => {
    it('renders the checked component', () => {
      const shallowWrapper = shallow(
        <Checkbox style={{}} checked onChange={() => true} />,
      );
      expect(shallowWrapper.dive().find(CheckboxChecked)).toExist();
    });
  });

  it('works with an onChange handler', () => {
    const mockAction = jest.fn();
    wrapper = mount(
      <Checkbox style={{}} checked={false} onChange={mockAction} />,
    );
    wrapper.find('Checkbox').first().simulate('click');
    expect(mockAction).toHaveBeenCalled();
  });

  it('renders custom Checkbox styles without melting', () => {
    wrapper = mount(
      <Checkbox onChange={() => true} checked={false} style={{ opacity: 1 }} />,
    );
    expect(wrapper.find('Checkbox')).toExist();
    expect(wrapper.find('Checkbox')).toHaveStyle({ opacity: 1 });
  });
});
