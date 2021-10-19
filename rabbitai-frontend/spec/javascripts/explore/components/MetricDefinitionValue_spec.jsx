/* eslint-disable no-unused-expressions */
import React from 'react';
import { shallow } from 'enzyme';

import { AGGREGATES } from 'src/explore/constants';
import MetricDefinitionValue from 'src/explore/components/controls/MetricControl/MetricDefinitionValue';
import AdhocMetricOption from 'src/explore/components/controls/MetricControl/AdhocMetricOption';
import AdhocMetric from 'src/explore/components/controls/MetricControl/AdhocMetric';

const sumValueAdhocMetric = new AdhocMetric({
  column: { type: 'DOUBLE', column_name: 'value' },
  aggregate: AGGREGATES.SUM,
});

describe('MetricDefinitionValue', () => {
  it('renders a MetricOption given a saved metric', () => {
    const wrapper = shallow(
      <MetricDefinitionValue
        onMetricEdit={() => {}}
        option={{ metric_name: 'a_saved_metric', expression: 'COUNT(*)' }}
        index={1}
      />,
    );
    expect(wrapper.find('AdhocMetricOption')).toExist();
  });

  it('renders an AdhocMetricOption given an adhoc metric', () => {
    const wrapper = shallow(
      <MetricDefinitionValue
        onMetricEdit={() => {}}
        option={sumValueAdhocMetric}
        index={1}
      />,
    );
    expect(wrapper.find(AdhocMetricOption)).toExist();
  });
});
