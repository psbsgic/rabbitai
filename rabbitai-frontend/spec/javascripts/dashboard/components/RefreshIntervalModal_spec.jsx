
import React from 'react';
import { mount } from 'enzyme';

import ModalTrigger from 'src/components/ModalTrigger';
import RefreshIntervalModal from 'src/dashboard/components/RefreshIntervalModal';
import Alert from 'src/components/Alert';
import { rabbitaiTheme, ThemeProvider } from '@rabbitai-ui/core';

const getMountWrapper = props =>
  mount(<RefreshIntervalModal {...props} />, {
    wrappingComponent: ThemeProvider,
    wrappingComponentProps: {
      theme: rabbitaiTheme,
    },
  });

describe('RefreshIntervalModal', () => {
  const mockedProps = {
    triggerNode: <i className="fa fa-edit" />,
    refreshFrequency: 10,
    onChange: jest.fn(),
    editMode: true,
  };
  it('is valid', () => {
    expect(
      React.isValidElement(<RefreshIntervalModal {...mockedProps} />),
    ).toBe(true);
  });
  it('renders the trigger node', () => {
    const wrapper = getMountWrapper(mockedProps);
    expect(wrapper.find('.fa-edit')).toExist();
  });
  it('should render a interval seconds', () => {
    const wrapper = getMountWrapper(mockedProps);
    expect(wrapper.prop('refreshFrequency')).toEqual(10);
  });
  it('should change refreshFrequency with edit mode', () => {
    const wrapper = getMountWrapper(mockedProps);
    wrapper.instance().handleFrequencyChange({ value: 30 });
    wrapper.instance().onSave();
    expect(mockedProps.onChange).toHaveBeenCalled();
    expect(mockedProps.onChange).toHaveBeenCalledWith(30, mockedProps.editMode);
  });
  it('should show warning message', () => {
    const props = {
      ...mockedProps,
      refreshLimit: 3600,
      refreshWarning: 'Show warning',
    };

    const wrapper = getMountWrapper(props);
    wrapper.find('span[role="button"]').simulate('click');

    wrapper.instance().handleFrequencyChange({ value: 30 });
    wrapper.update();
    expect(wrapper.find(ModalTrigger).find(Alert)).toExist();

    wrapper.instance().handleFrequencyChange({ value: 3601 });
    wrapper.update();
    expect(wrapper.find(ModalTrigger).find(Alert)).not.toExist();
  });
});
