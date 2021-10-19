import React from 'react';
import IndeterminateCheckbox, { IndeterminateCheckboxProps } from '.';

export default {
  title: 'IndeterminateCheckbox',
  component: IndeterminateCheckbox,
};

export const InteractiveIndeterminateCheckbox = (
  args: IndeterminateCheckboxProps,
) => <IndeterminateCheckbox {...args} />;

InteractiveIndeterminateCheckbox.args = {
  checked: false,
  id: 'checkbox-id',
  indeterminate: false,
  title: 'Checkbox title',
  onChange: () => null,
};

InteractiveIndeterminateCheckbox.story = {
  parameters: {
    knobs: {
      disable: true,
    },
  },
};
