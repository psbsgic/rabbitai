
import React, { useState } from 'react';
import PopoverDropdown, { PopoverDropdownProps, OptionProps } from '.';

export default {
  title: 'PopoverDropdown',
  includeStories: ['InteractivePopoverDropdown'],
};

export const OPTIONS: OptionProps[] = [
  { label: 'Option A', value: 'A' },
  { label: 'Option B', value: 'B' },
  { label: 'Option C', value: 'C' },
];

type ElementType = 'default' | 'button';

type Props = PopoverDropdownProps & {
  buttonType: ElementType;
  optionType: ElementType;
};

export const InteractivePopoverDropdown = (props: Props) => {
  const { value, buttonType, optionType, ...rest } = props;
  const [currentValue, setCurrentValue] = useState(value);

  const newElementHandler = (type: ElementType) => ({
    label,
    value,
  }: OptionProps) => {
    if (type === 'button') {
      return (
        <button type="button" key={value}>
          {label}
        </button>
      );
    }
    return <span>{label}</span>;
  };

  return (
    <PopoverDropdown
      {...rest}
      value={currentValue}
      renderButton={newElementHandler(buttonType)}
      renderOption={newElementHandler(optionType)}
      onChange={selected => setCurrentValue(selected as string)}
    />
  );
};

InteractivePopoverDropdown.argTypes = {
  buttonType: {
    defaultValue: 'default',
    control: { type: 'radio', options: ['default', 'button'] },
  },
  optionType: {
    defaultValue: 'default',
    control: { type: 'radio', options: ['default', 'button'] },
  },
  value: {
    defaultValue: OPTIONS[0].value,
    table: { disable: true },
  },
  options: {
    defaultValue: OPTIONS,
    table: { disable: true },
  },
};

InteractivePopoverDropdown.story = {
  parameters: {
    knobs: {
      disable: true,
    },
  },
};
