/* eslint-disable no-unused-expressions */
import React from 'react';
import sinon from 'sinon';
import { shallow } from 'enzyme';
import { Tooltip } from 'src/components/Tooltip';

import AdhocMetricEditPopoverTitle from 'src/explore/components/controls/MetricControl/AdhocMetricEditPopoverTitle';

const title = {
  label: 'Title',
  hasCustomLabel: false,
};

function setup(overrides) {
  const onChange = sinon.spy();
  const props = {
    title,
    onChange,
    ...overrides,
  };
  const wrapper = shallow(<AdhocMetricEditPopoverTitle {...props} />);
  return { wrapper, onChange };
}

describe('AdhocMetricEditPopoverTitle', () => {
  it('renders an OverlayTrigger wrapper with the title', () => {
    const { wrapper } = setup();
    expect(wrapper.find(Tooltip)).toExist();
    expect(
      wrapper.find('[data-test="AdhocMetricEditTitle#trigger"]').text(),
    ).toBe(`${title.label}\xa0`);
  });

  it('transfers to edit mode when clicked', () => {
    const { wrapper } = setup();
    expect(wrapper.state('isEditMode')).toBe(false);
    wrapper
      .find('[data-test="AdhocMetricEditTitle#trigger"]')
      .simulate('click');
    expect(wrapper.state('isEditMode')).toBe(true);
  });

  it('Render non-interactive span with title when edit is disabled', () => {
    const { wrapper } = setup({ isEditDisabled: true });
    expect(
      wrapper.find('[data-test="AdhocMetricTitle"]').exists(),
    ).toBeTruthy();
    expect(
      wrapper.find('[data-test="AdhocMetricEditTitle#trigger"]').exists(),
    ).toBeFalsy();
  });
});
