/* eslint-disable no-unused-expressions */
import React from 'react';
import { shallow } from 'enzyme';
import { styledMount as mount } from 'spec/helpers/theming';
import FilterDefinitionOption from 'src/explore/components/controls/MetricControl/FilterDefinitionOption';
import { AGGREGATES } from 'src/explore/constants';
import AdhocMetric, {
  EXPRESSION_TYPES,
} from 'src/explore/components/controls/MetricControl/AdhocMetric';
import { StyledColumnOption } from 'src/explore/components/optionRenderers';

const sumValueAdhocMetric = new AdhocMetric({
  expressionType: EXPRESSION_TYPES.SIMPLE,
  column: { type: 'VARCHAR(255)', column_name: 'source' },
  aggregate: AGGREGATES.SUM,
});

describe('FilterDefinitionOption', () => {
  it('renders a StyledColumnOption given a column', () => {
    const wrapper = shallow(
      <FilterDefinitionOption option={{ column_name: 'a_column' }} />,
    );
    expect(wrapper.find(StyledColumnOption)).toExist();
  });

  it('renders a StyledColumnOption given an adhoc metric', () => {
    const wrapper = shallow(
      <FilterDefinitionOption option={sumValueAdhocMetric} />,
    );
    expect(wrapper.find(StyledColumnOption)).toExist();
  });

  it('renders the metric name given a saved metric', () => {
    const wrapper = mount(
      <FilterDefinitionOption
        option={{ saved_metric_name: 'my_custom_metric' }}
      />,
    );
    expect(wrapper.find('.option-label').text()).toBe('my_custom_metric');
  });
});
