
import React from 'react';
import { shallow } from 'enzyme';
import { styledMount as mount } from 'spec/helpers/theming';
import FilterBox from 'src/visualizations/FilterBox/FilterBox';
import SelectControl from 'src/explore/components/controls/SelectControl';

describe('FilterBox', () => {
  it('should only add defined non-predefined options to filtersChoices', () => {
    const wrapper = shallow(
      <FilterBox
        chartId={1001}
        datasource={{ id: 1 }}
        filtersChoices={{
          name: [
            { id: 'John', text: 'John', metric: 1234 },
            { id: 'Jane', text: 'Jane', metric: 345678 },
          ],
        }}
        filtersFields={[
          {
            asc: false,
            clearable: true,
            column: 'name',
            key: 'name',
            label: 'name',
            metric: 'sum__COUNT',
            multiple: true,
          },
        ]}
        origSelectedValues={{}}
      />,
    );
    const inst = wrapper.instance();
    // choose a predefined value
    inst.setState({ selectedValues: { name: ['John'] } });
    expect(inst.props.filtersChoices.name.length).toEqual(2);
    // reset selection
    inst.setState({ selectedValues: { name: null } });
    expect(inst.props.filtersChoices.name.length).toEqual(2);
    // Add a new name
    inst.setState({ selectedValues: { name: 'James' } });
    expect(inst.props.filtersChoices.name.length).toEqual(3);
  });

  it('should support granularity_sqla options', () => {
    const wrapper = mount(
      <FilterBox
        chartId={1001}
        datasource={{
          id: 1,
          columns: [],
          databases: {},
          granularity_sqla: [
            ['created_on', 'created_on'],
            ['changed_on', 'changed_on'],
          ],
        }}
        showSqlaTimeColumn
        instantFiltering
      />,
    );

    expect(wrapper.find(SelectControl).props().choices).toEqual(
      expect.arrayContaining([
        ['created_on', 'created_on'],
        ['changed_on', 'changed_on'],
      ]),
    );
  });
});
