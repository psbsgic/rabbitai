import React from 'react';
import { ReactWrapper } from 'enzyme';
import { styledMount as mount } from 'spec/helpers/theming';
import { CronPicker } from 'src/components/CronPicker';
import { Input } from 'src/common/components';

import { AlertReportCronScheduler } from './AlertReportCronScheduler';

describe('AlertReportCronScheduler', () => {
  let wrapper: ReactWrapper;

  it('calls onChnage when value chnages', () => {
    const onChangeMock = jest.fn();
    wrapper = mount(
      <AlertReportCronScheduler value="* * * * *" onChange={onChangeMock} />,
    );

    const changeValue = '1,7 * * * *';

    wrapper.find(CronPicker).props().setValue(changeValue);
    expect(onChangeMock).toHaveBeenLastCalledWith(changeValue);
  });

  it.skip('sets input value when cron picker changes', () => {
    const onChangeMock = jest.fn();
    wrapper = mount(
      <AlertReportCronScheduler value="* * * * *" onChange={onChangeMock} />,
    );

    const changeValue = '1,7 * * * *';

    wrapper.find(CronPicker).props().setValue(changeValue);
    // TODO fix this class-style assertion that doesn't work on function components
    // @ts-ignore
    expect(wrapper.find(Input).state().value).toEqual(changeValue);
  });

  it('calls onChange when input value changes', () => {
    const onChangeMock = jest.fn();
    wrapper = mount(
      <AlertReportCronScheduler value="* * * * *" onChange={onChangeMock} />,
    );

    const changeValue = '1,7 * * * *';
    const event = {
      target: { value: changeValue },
    } as React.FocusEvent<HTMLInputElement>;

    const inputProps = wrapper.find(Input).props();
    if (inputProps.onBlur) {
      inputProps.onBlur(event);
    }
    expect(onChangeMock).toHaveBeenLastCalledWith(changeValue);
  });
});
