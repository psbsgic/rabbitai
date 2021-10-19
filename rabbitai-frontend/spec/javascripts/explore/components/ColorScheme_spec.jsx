/* eslint-disable no-unused-expressions */
import React from 'react';
import { Select } from 'src/components';
import { getCategoricalSchemeRegistry } from '@superset-ui/core';
import { styledMount as mount } from 'spec/helpers/theming';
import ColorSchemeControl from 'src/explore/components/controls/ColorSchemeControl';

const defaultProps = {
  name: 'color_scheme',
  label: 'Color Scheme',
  options: getCategoricalSchemeRegistry()
    .keys()
    .map(s => [s, s]),
};

describe('ColorSchemeControl', () => {
  let wrapper;
  beforeEach(() => {
    wrapper = mount(<ColorSchemeControl {...defaultProps} />);
  });

  it('renders a Select', () => {
    expect(wrapper.find(Select)).toExist();
  });
});
