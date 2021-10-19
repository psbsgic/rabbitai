import React from 'react';
import { DatePickerProps, RangePickerProps } from 'antd/lib/date-picker';
import { DatePicker, RangePicker } from '.';

export default {
  title: 'DatePicker',
  component: DatePicker,
};

const commonArgs = {
  allowClear: true,
  autoFocus: true,
  bordered: true,
  disabled: false,
  inputReadOnly: false,
  size: 'middle',
  format: 'YYYY-MM-DD hh:mm a',
  showTime: { format: 'hh:mm a' },
};

const interactiveTypes = {
  mode: { disabled: true },
  picker: {
    control: {
      type: 'select',
      options: ['', 'date', 'week', 'month', 'quarter', 'year'],
    },
  },
  size: {
    control: {
      type: 'select',
      options: ['large', 'middle', 'small'],
    },
  },
};

export const InteractiveDatePicker = (args: DatePickerProps) => (
  <DatePicker {...args} />
);

InteractiveDatePicker.args = {
  ...commonArgs,
  picker: 'date',
  placeholder: 'Placeholder',
  showToday: true,
};

InteractiveDatePicker.argTypes = interactiveTypes;

InteractiveDatePicker.story = {
  parameters: {
    knobs: {
      disable: true,
    },
  },
};

export const InteractiveRangePicker = (args: RangePickerProps) => (
  <RangePicker {...args} />
);

InteractiveRangePicker.args = {
  ...commonArgs,
  allowEmpty: true,
  showNow: true,
  separator: '-',
};

InteractiveRangePicker.argTypes = interactiveTypes;

InteractiveRangePicker.story = {
  parameters: {
    knobs: {
      disable: true,
    },
  },
};
