/* eslint-disable no-unused-expressions */
import React from 'react';
import sinon from 'sinon';
import { mount } from 'enzyme';
import { ThemeProvider, supersetTheme } from '@superset-ui/core';
import CheckboxControl from 'src/explore/components/controls/CheckboxControl';
import ControlHeader from 'src/explore/components/ControlHeader';
import Checkbox from 'src/components/Checkbox';

const defaultProps = {
  name: 'show_legend',
  onChange: sinon.spy(),
  value: false,
  label: 'checkbox label',
};

describe('CheckboxControl', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = mount(
      <ThemeProvider theme={supersetTheme}>
        <CheckboxControl {...defaultProps} />
      </ThemeProvider>,
    );
  });

  it('renders a Checkbox', () => {
    const controlHeader = wrapper.childAt(0).find(ControlHeader);
    expect(controlHeader).toHaveLength(1);
    expect(controlHeader.find(Checkbox)).toHaveLength(1);
  });

  it('Checks the box when the label is clicked', () => {
    const fullComponent = wrapper.childAt(0);
    const spy = sinon.spy(fullComponent.instance(), 'onChange');

    fullComponent.instance().forceUpdate();

    fullComponent.find('label span').last().simulate('click');

    expect(spy.calledOnce).toBe(true);
  });
});
