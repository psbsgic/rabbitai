import React from 'react';
import { useArgs } from '@storybook/client-api';
import { Switch, SwitchProps } from '.';

export default {
  title: 'Switch',
};

export const InteractiveSwitch = ({ checked, ...rest }: SwitchProps) => {
  const [, updateArgs] = useArgs();
  return (
    <Switch
      {...rest}
      checked={checked}
      onChange={value => updateArgs({ checked: value })}
    />
  );
};

InteractiveSwitch.args = {
  checked: false,
  disabled: false,
  loading: false,
  title: 'Switch',
};

InteractiveSwitch.argTypes = {
  size: {
    defaultValue: 'default',
    control: { type: 'radio', options: ['small', 'default'] },
  },
};

InteractiveSwitch.story = {
  parameters: {
    knobs: {
      disable: true,
    },
  },
};
