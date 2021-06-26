

import React from 'react';
import { ReactWrapper } from 'enzyme';
import { styledMount as mount } from 'spec/helpers/theming';
import Label from '.';
import { LabelGallery, options } from './Label.stories';

describe('Label', () => {
  let wrapper: ReactWrapper;

  // test the basic component
  it('renders the base component (no onClick)', () => {
    expect(React.isValidElement(<Label />)).toBe(true);
  });

  it('works with an onClick handler', () => {
    const mockAction = jest.fn();
    wrapper = mount(<Label onClick={mockAction} />);
    wrapper.find(Label).simulate('click');
    expect(mockAction).toHaveBeenCalled();
  });

  // test stories from the storybook!
  it('renders all the storybook gallery variants', () => {
    wrapper = mount(<LabelGallery />);
    expect(wrapper.find(Label).length).toEqual(options.length * 2);
  });
});
