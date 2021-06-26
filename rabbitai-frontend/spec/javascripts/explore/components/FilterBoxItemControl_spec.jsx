
/* eslint-disable no-unused-expressions */
import React from 'react';
import sinon from 'sinon';
import { shallow } from 'enzyme';

import Popover from 'src/components/Popover';
import FilterBoxItemControl from 'src/explore/components/controls/FilterBoxItemControl';
import FormRow from 'src/components/FormRow';
import datasources from 'spec/fixtures/mockDatasource';

const defaultProps = {
  label: 'some label',
  datasource: datasources['7__table'],
  onChange: sinon.spy(),
};

describe('FilterBoxItemControl', () => {
  let wrapper;
  let inst;

  const getWrapper = propOverrides => {
    const props = { ...defaultProps, ...propOverrides };
    return shallow(<FilterBoxItemControl {...props} />);
  };
  beforeEach(() => {
    wrapper = getWrapper();
    inst = wrapper.instance();
  });

  it('renders a Popover', () => {
    expect(wrapper.find(Popover)).toExist();
  });

  it('renderForms does the job', () => {
    const popover = shallow(inst.renderForm());
    expect(popover.find(FormRow)).toHaveLength(8);
    expect(popover.find(FormRow).get(1).props.control.props.value).toEqual(
      'some label',
    );
  });

  it('convert type for single value filter_box', () => {
    inst = getWrapper({
      datasource: {
        columns: [
          {
            column_name: 'SP_POP_TOTL',
            description: null,
            expression: null,
            filterable: true,
            groupby: true,
            id: 312,
            is_dttm: false,
            type: 'FLOAT',
            verbose_name: null,
          },
        ],
        metrics: [
          {
            d3format: null,
            description: null,
            expression: 'sum("SP_POP_TOTL")',
            id: 3,
            metric_name: 'sum__SP_POP_TOTL',
            verbose_name: null,
            warning_text: null,
          },
        ],
      },
    }).instance();
    inst.setState({
      asc: true,
      clearable: true,
      column: 'SP_POP_TOTL',
      defaultValue: 254454778,
      metric: undefined,
      multiple: false,
    });
    inst.setState = sinon.spy();

    inst.onControlChange('defaultValue', '1');
    expect(inst.setState.callCount).toBe(1);
    expect(inst.setState.getCall(0).args[0]).toEqual({ defaultValue: 1 });

    // user input is invalid for number type column
    inst.onControlChange('defaultValue', 'abc');
    expect(inst.setState.callCount).toBe(2);
    expect(inst.setState.getCall(1).args[0]).toEqual({ defaultValue: null });
  });
});
