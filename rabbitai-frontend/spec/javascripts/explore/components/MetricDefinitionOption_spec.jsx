import React from 'react';
import configureStore from 'redux-mock-store';
import { shallow } from 'enzyme';

import MetricDefinitionOption from 'src/explore/components/controls/MetricControl/MetricDefinitionOption';
import AggregateOption from 'src/explore/components/controls/MetricControl/AggregateOption';
import {
  StyledMetricOption,
  StyledColumnOption,
} from 'src/explore/components/optionRenderers';

describe('MetricDefinitionOption', () => {
  const mockStore = configureStore([]);
  const store = mockStore({});

  function setup(props) {
    return shallow(<MetricDefinitionOption store={store} {...props} />).dive();
  }

  it('renders a StyledMetricOption given a saved metric', () => {
    const wrapper = setup({
      option: { metric_name: 'a_saved_metric', expression: 'COUNT(*)' },
    });
    expect(wrapper.find(StyledMetricOption)).toExist();
  });

  it('renders a StyledColumnOption given a column', () => {
    const wrapper = setup({ option: { column_name: 'a_column' } });
    expect(wrapper.find(StyledColumnOption)).toExist();
  });

  it('renders an AggregateOption given an aggregate metric', () => {
    const wrapper = setup({ option: { aggregate_name: 'an_aggregate' } });
    expect(wrapper.find(AggregateOption)).toExist();
  });
});
