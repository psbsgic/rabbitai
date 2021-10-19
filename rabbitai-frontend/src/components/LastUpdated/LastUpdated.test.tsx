import React from 'react';
import { ReactWrapper } from 'enzyme';
import { styledMount as mount } from 'spec/helpers/theming';
import LastUpdated from '.';

describe('LastUpdated', () => {
  let wrapper: ReactWrapper;
  const updatedAt = new Date('Sat Dec 12 2020 00:00:00 GMT-0800');

  it('renders the base component (no refresh)', () => {
    const wrapper = mount(<LastUpdated updatedAt={updatedAt} />);
    expect(/^Last Updated .+$/.test(wrapper.text())).toBe(true);
  });

  it('renders a refresh action', () => {
    const mockAction = jest.fn();
    wrapper = mount(<LastUpdated updatedAt={updatedAt} update={mockAction} />);
    const props = wrapper.find('[aria-label="refresh"]').first().props();
    if (props.onClick) {
      props.onClick({} as React.MouseEvent);
    }
    expect(mockAction).toHaveBeenCalled();
  });
});
