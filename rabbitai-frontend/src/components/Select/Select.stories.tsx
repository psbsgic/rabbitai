
import React from 'react';
import { useArgs } from '@storybook/client-api';
import { OptionTypeBase } from 'react-select';
import Select from '.';

const OPTIONS = [
  { label: 'Blue', value: 'blue' },
  { label: 'Red', value: 'red' },
  { label: 'Orange', value: 'orange' },
];

export default {
  title: 'Select',
  argTypes: {
    options: {
      type: 'select',
      options: OPTIONS,
    },
    multi: {
      type: 'boolean',
    },
    value: {
      type: 'string',
    },
    clearable: {
      type: 'boolean',
    },
    placeholder: {
      type: 'string',
    },
  },
};

export const SelectGallery = ({ value }: { value: OptionTypeBase }) => (
  <>
    <h4>With default value</h4>
    <Select
      value={OPTIONS[0]}
      ignoreAccents={false}
      name="select-datasource"
      onChange={() => {}}
      options={OPTIONS}
      placeholder="choose one"
      width={600}
    />
    <hr />
    <h4>With no value</h4>
    <Select
      ignoreAccents={false}
      name="select-datasource"
      onChange={() => {}}
      options={OPTIONS}
      placeholder="choose one"
      width={600}
      value={value}
    />
    <hr />
    <h4>Multi select</h4>
    <Select
      ignoreAccents={false}
      name="select-datasource"
      onChange={() => {}}
      options={OPTIONS}
      placeholder="choose one or more values"
      width={600}
      value={[OPTIONS[0]]}
      multi
    />
  </>
);

SelectGallery.args = {
  value: '',
  options: OPTIONS,
};

SelectGallery.story = {
  parameters: {
    knobs: {
      disabled: true,
    },
  },
};

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const InteractiveSelect = (args: any) => {
  const [{ value, multi, clearable, placeholder }, updateArgs] = useArgs();
  const onSelect = (selection: {}) => {
    const { value }: { value?: any } = selection || {};
    if (multi) {
      updateArgs({ value: selection });
      return;
    }
    updateArgs({ value });
  };

  return (
    <Select
      clearable={clearable}
      onChange={onSelect}
      name="interactive-select"
      options={OPTIONS}
      placeholder={placeholder}
      with={600}
      value={value}
      multi={multi}
    />
  );
};

InteractiveSelect.args = {
  value: '',
  multi: false,
  options: OPTIONS,
  clearable: false,
  placeholder: "I'm interactive",
};

InteractiveSelect.story = {
  parameters: {
    knobs: {
      disabled: true,
    },
  },
};
