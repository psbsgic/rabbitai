
/* eslint-disable no-unused-expressions */
import React from 'react';
import sinon from 'sinon';
import { shallow } from 'enzyme';

import Popover from 'src/components/Popover';
import { AGGREGATES } from 'src/explore/constants';
import AdhocMetricOption from 'src/explore/components/controls/MetricControl/AdhocMetricOption';
import AdhocMetric from 'src/explore/components/controls/MetricControl/AdhocMetric';

const columns = [
  { type: 'VARCHAR(255)', column_name: 'source' },
  { type: 'VARCHAR(255)', column_name: 'target' },
  { type: 'DOUBLE', column_name: 'value' },
];

const sumValueAdhocMetric = new AdhocMetric({
  column: columns[2],
  aggregate: AGGREGATES.SUM,
});

function setup(overrides) {
  const onMetricEdit = sinon.spy();
  const props = {
    adhocMetric: sumValueAdhocMetric,
    savedMetric: {},
    savedMetrics: [],
    onMetricEdit,
    columns,
    onMoveLabel: () => {},
    onDropLabel: () => {},
    index: 0,
    ...overrides,
  };
  const wrapper = shallow(<AdhocMetricOption {...props} />)
    .find('AdhocMetricPopoverTrigger')
    .shallow();
  return { wrapper, onMetricEdit };
}

describe('AdhocMetricOption', () => {
  it('renders an overlay trigger wrapper for the label', () => {
    const { wrapper } = setup();
    expect(wrapper.find(Popover)).toExist();
    expect(wrapper.find('OptionControlLabel')).toExist();
  });

  it('overwrites the adhocMetric in state with onLabelChange', () => {
    const { wrapper } = setup();
    wrapper.instance().onLabelChange({ target: { value: 'new label' } });
    expect(wrapper.state('title').label).toBe('new label');
    expect(wrapper.state('title').hasCustomLabel).toBe(true);
  });

  it('returns to default labels when the custom label is cleared', () => {
    const { wrapper } = setup();
    expect(wrapper.state('title').label).toBe('SUM(value)');

    wrapper.instance().onLabelChange({ target: { value: 'new label' } });
    expect(wrapper.state('title').label).toBe('new label');

    wrapper.instance().onLabelChange({ target: { value: '' } });

    expect(wrapper.state('title').label).toBe('SUM(value)');
    expect(wrapper.state('title').hasCustomLabel).toBe(false);
  });
});
