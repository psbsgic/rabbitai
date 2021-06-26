
import React from 'react';
import { shallow } from 'enzyme';

import ResizableHandle from 'src/dashboard/components/resizable/ResizableHandle';

/* eslint-disable react/jsx-pascal-case */
describe('ResizableHandle', () => {
  it('should render a right resize handle', () => {
    const wrapper = shallow(<ResizableHandle.right />);
    expect(wrapper.find('.resize-handle.resize-handle--right')).toExist();
  });

  it('should render a bottom resize handle', () => {
    const wrapper = shallow(<ResizableHandle.bottom />);
    expect(wrapper.find('.resize-handle.resize-handle--bottom')).toHaveLength(
      1,
    );
  });

  it('should render a bottomRight resize handle', () => {
    const wrapper = shallow(<ResizableHandle.bottomRight />);
    expect(
      wrapper.find('.resize-handle.resize-handle--bottom-right'),
    ).toHaveLength(1);
  });
});
/* eslint-enable react/jsx-pascal-case */
