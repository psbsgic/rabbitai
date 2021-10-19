import React from 'react';
import { shallow } from 'enzyme';

import { ExploreChartHeader } from 'src/explore/components/ExploreChartHeader';
import ExploreActionButtons from 'src/explore/components/ExploreActionButtons';
import EditableTitle from 'src/components/EditableTitle';

const saveSliceStub = jest.fn();
const updateChartTitleStub = jest.fn();
const fetchUISpecificReportStub = jest.fn();
const mockProps = {
  actions: {
    saveSlice: saveSliceStub,
    updateChartTitle: updateChartTitleStub,
  },
  can_overwrite: true,
  can_download: true,
  isStarred: true,
  slice: {
    form_data: {
      viz_type: 'line',
    },
  },
  table_name: 'foo',
  form_data: {
    viz_type: 'table',
  },
  user: {
    createdOn: '2021-04-27T18:12:38.952304',
    email: 'admin',
    firstName: 'admin',
    isActive: true,
    lastName: 'admin',
    permissions: {},
    roles: { Admin: Array(173) },
    userId: 1,
    username: 'admin',
  },
  timeout: 1000,
  chart: {
    id: 0,
    queryResponse: {},
  },
  fetchUISpecificReport: fetchUISpecificReportStub,
  chartHeight: '30px',
};

describe('ExploreChartHeader', () => {
  let wrapper;
  beforeEach(() => {
    wrapper = shallow(<ExploreChartHeader {...mockProps} />);
  });

  it('is valid', () => {
    expect(React.isValidElement(<ExploreChartHeader {...mockProps} />)).toBe(
      true,
    );
  });

  it('renders', () => {
    expect(wrapper.find(EditableTitle)).toExist();
    expect(wrapper.find(ExploreActionButtons)).toExist();
  });

  it('should update title but not save', () => {
    const editableTitle = wrapper.find(EditableTitle);
    expect(editableTitle.props().onSaveTitle).toBe(updateChartTitleStub);
  });
});
