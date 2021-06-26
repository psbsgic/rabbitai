
import React from 'react';
import TextControl from 'src/explore/components/controls/TextControl';
import CheckboxControl from 'src/explore/components/controls/CheckboxControl';
import FormRow from '.';

export default {
  title: 'FormRow',
};

export const InteractiveFormRow = ({ isCheckbox, ...rest }: any) => {
  const control = isCheckbox ? (
    <CheckboxControl label="Checkbox" />
  ) : (
    <TextControl />
  );
  return (
    <div style={{ width: 300 }}>
      <FormRow {...rest} control={control} isCheckbox={isCheckbox} />
    </div>
  );
};

InteractiveFormRow.args = {
  label: 'Label',
  tooltip: 'Tooltip',
  control: <TextControl />,
  isCheckbox: false,
};

InteractiveFormRow.argTypes = {
  control: {
    defaultValue: <TextControl />,
    table: {
      disable: true,
    },
  },
};

InteractiveFormRow.story = {
  parameters: {
    knobs: {
      disable: true,
    },
  },
};
