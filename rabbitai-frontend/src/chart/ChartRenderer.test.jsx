import React from 'react';
import { shallow } from 'enzyme';
import { SuperChart } from '@superset-ui/core';

import ChartRenderer from 'src/chart/ChartRenderer';

const requiredProps = {
  chartId: 1,
  datasource: {},
  formData: {},
  vizType: 'foo',
};

describe('ChartRenderer', () => {
  it('should render SuperChart', () => {
    const wrapper = shallow(
      <ChartRenderer {...requiredProps} refreshOverlayVisible={false} />,
    );
    expect(wrapper.find(SuperChart)).toExist();
  });

  it('should not render SuperChart when refreshOverlayVisible is true', () => {
    const wrapper = shallow(
      <ChartRenderer {...requiredProps} refreshOverlayVisible />,
    );
    expect(wrapper.find(SuperChart)).not.toExist();
  });
});
