
import React from 'react';
import sinon from 'sinon';
import { shallow } from 'enzyme';

import TabStatusIcon from 'src/SqlLab/components/TabStatusIcon';

function setup() {
  const onClose = sinon.spy();
  const wrapper = shallow(
    <TabStatusIcon onClose={onClose} tabState="running" />,
  );
  return { wrapper, onClose };
}

describe('TabStatusIcon', () => {
  it('renders a circle without an x when hovered', () => {
    const { wrapper } = setup();
    expect(wrapper.find('div.circle')).toExist();
    expect(wrapper.text()).toBe('');
  });
});
