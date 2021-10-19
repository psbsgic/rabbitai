/* eslint-disable no-unused-expressions */
import React from 'react';
import sinon from 'sinon';
import { shallow } from 'enzyme';
import { TextAreaEditor } from 'src/components/AsyncAceEditor';
import { TextArea } from 'src/common/components';

import TextAreaControl from 'src/explore/components/controls/TextAreaControl';

const defaultProps = {
  name: 'x_axis_label',
  label: 'X Axis Label',
  onChange: sinon.spy(),
};

describe('SelectControl', () => {
  let wrapper;
  beforeEach(() => {
    wrapper = shallow(<TextAreaControl {...defaultProps} />);
  });

  it('renders a FormControl', () => {
    expect(wrapper.find(TextArea)).toExist();
  });

  it('calls onChange when toggled', () => {
    const select = wrapper.find(TextArea);
    select.simulate('change', { target: { value: 'x' } });
    expect(defaultProps.onChange.calledWith('x')).toBe(true);
  });

  it('renders a AceEditor when language is specified', () => {
    const props = { ...defaultProps };
    props.language = 'markdown';
    wrapper = shallow(<TextAreaControl {...props} />);
    expect(wrapper.find(TextArea)).not.toExist();
    expect(wrapper.find(TextAreaEditor)).toExist();
  });
});
