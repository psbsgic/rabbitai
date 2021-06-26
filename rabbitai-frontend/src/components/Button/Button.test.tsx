

import React from 'react';
import { ReactWrapper } from 'enzyme';
import { styledMount as mount } from 'spec/helpers/theming';
import Button from '.';
import {
  ButtonGallery,
  SIZES as buttonSizes,
  STYLES as buttonStyles,
} from './Button.stories';

describe('Button', () => {
  let wrapper: ReactWrapper;

  // test the basic component
  it('renders the base component', () => {
    expect(React.isValidElement(<Button />)).toBe(true);
  });

  it('works with an onClick handler', () => {
    const mockAction = jest.fn();
    wrapper = mount(<Button onClick={mockAction} />);
    wrapper.find('Button').first().simulate('click');
    expect(mockAction).toHaveBeenCalled();
  });

  it('does not handle onClicks when disabled', () => {
    const mockAction = jest.fn();
    wrapper = mount(<Button onClick={mockAction} disabled />);
    wrapper.find('Button').first().simulate('click');
    expect(mockAction).toHaveBeenCalledTimes(0);
  });

  // test stories from the storybook!
  it('All the sorybook gallery variants mount', () => {
    wrapper = mount(<ButtonGallery />);

    const permutationCount =
      Object.values(buttonStyles.options).filter(o => o).length *
      Object.values(buttonSizes.options).length;

    expect(wrapper.find(Button).length).toEqual(permutationCount);
  });
});
