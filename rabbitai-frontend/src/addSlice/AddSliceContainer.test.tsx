import React from 'react';
import { ReactWrapper } from 'enzyme';
import Button from 'src/components/Button';
import { Select } from 'src/components';
import AddSliceContainer, {
  AddSliceContainerProps,
  AddSliceContainerState,
} from 'src/addSlice/AddSliceContainer';
import VizTypeGallery from 'src/explore/components/controls/VizTypeControl/VizTypeGallery';
import { styledMount as mount } from 'spec/helpers/theming';
import { act } from 'spec/helpers/testing-library';

const defaultProps = {
  datasources: [
    { label: 'my first table', value: '1__table' },
    { label: 'another great table', value: '2__table' },
  ],
};

describe('AddSliceContainer', () => {
  let wrapper: ReactWrapper<
    AddSliceContainerProps,
    AddSliceContainerState,
    AddSliceContainer
  >;

  beforeEach(async () => {
    wrapper = mount(<AddSliceContainer {...defaultProps} />) as ReactWrapper<
      AddSliceContainerProps,
      AddSliceContainerState,
      AddSliceContainer
    >;
    // suppress a warning caused by some unusual async behavior in Icon
    await act(() => new Promise(resolve => setTimeout(resolve, 0)));
  });

  it('renders a select and a VizTypeControl', () => {
    expect(wrapper.find(Select)).toExist();
    expect(wrapper.find(VizTypeGallery)).toExist();
  });

  it('renders a button', () => {
    expect(wrapper.find(Button)).toExist();
  });

  it('renders a disabled button if no datasource is selected', () => {
    expect(
      wrapper.find(Button).find({ disabled: true }).hostNodes(),
    ).toHaveLength(1);
  });

  it('renders an enabled button if datasource and viz type is selected', () => {
    const datasourceValue = defaultProps.datasources[0].value;
    wrapper.setState({
      datasourceValue,
      datasourceId: datasourceValue.split('__')[0],
      datasourceType: datasourceValue.split('__')[1],
      visType: 'table',
    });
    expect(
      wrapper.find(Button).find({ disabled: true }).hostNodes(),
    ).toHaveLength(0);
  });

  it('formats explore url', () => {
    const datasourceValue = defaultProps.datasources[0].value;
    wrapper.setState({
      datasourceValue,
      datasourceId: datasourceValue.split('__')[0],
      datasourceType: datasourceValue.split('__')[1],
      visType: 'table',
    });
    const formattedUrl =
      '/rabbitai/explore/?form_data=%7B%22viz_type%22%3A%22table%22%2C%22datasource%22%3A%221__table%22%7D';
    expect(wrapper.instance().exploreUrl()).toBe(formattedUrl);
  });
});
