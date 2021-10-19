import React from 'react';
import { shallow } from 'enzyme';

import MissingChart from 'src/dashboard/components/MissingChart';

describe('MissingChart', () => {
  function setup(overrideProps) {
    const wrapper = shallow(<MissingChart height={100} {...overrideProps} />);
    return wrapper;
  }

  it('renders a .missing-chart-container', () => {
    const wrapper = setup();
    expect(wrapper.find('.missing-chart-container')).toExist();
  });

  it('renders a .missing-chart-body', () => {
    const wrapper = setup();
    expect(wrapper.find('.missing-chart-body')).toExist();
  });
});
