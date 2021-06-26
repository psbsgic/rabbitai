
import React, { useState } from 'react';
import LabeledErrorBoundInput, {
  LabeledErrorBoundInputProps,
} from './LabeledErrorBoundInput';

export default {
  title: 'LabeledErrorBoundInput',
  component: LabeledErrorBoundInput,
};

export const InteractiveLabeledErrorBoundInput = ({
  name,
  value,
  placeholder,
  type,
  id,
}: LabeledErrorBoundInputProps) => {
  const [currentValue, setCurrentValue] = useState(value);

  const validateFunctionality: (value: any) => string = value => {
    setCurrentValue(value.target.value);
    if (value.target.value.includes('success')) {
      return 'success';
    }
    return 'error';
  };

  return (
    <LabeledErrorBoundInput
      id={id}
      name={name}
      validationMethods={{ onChange: validateFunctionality }}
      errorMessage={
        currentValue === 'success' ? '' : 'Type success in the text bar'
      }
      helpText="This is a line of example help text"
      value={currentValue}
      // This must stay the same as name or form breaks
      label={name}
      placeholder={placeholder}
      type={type}
      required
    />
  );
};

InteractiveLabeledErrorBoundInput.args = {
  name: 'Username',
  placeholder: 'Example placeholder text...',
  id: 1,
};

InteractiveLabeledErrorBoundInput.argTypes = {
  type: {
    defaultValue: 'textbox',
    control: {
      type: 'select',
      options: ['textbox', 'checkbox', 'radio'],
    },
  },
};
