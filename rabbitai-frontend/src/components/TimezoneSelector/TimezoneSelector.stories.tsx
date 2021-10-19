import React from 'react';
import { useArgs } from '@storybook/client-api';
import TimezoneSelector, { TimezoneProps } from './index';

export default {
  title: 'TimezoneSelector',
  component: TimezoneSelector,
};

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const InteractiveTimezoneSelector = (args: TimezoneProps) => {
  const [{ timezone }, updateArgs] = useArgs();
  const onTimezoneChange = (value: string) => {
    updateArgs({ timezone: value });
  };
  return (
    <TimezoneSelector timezone={timezone} onTimezoneChange={onTimezoneChange} />
  );
};

InteractiveTimezoneSelector.args = {
  timezone: 'America/Los_Angeles',
};
