import React, { useState, useRef, useCallback } from 'react';
import { Input, Divider } from 'src/common/components';
import { CronPicker, CronError, CronProps } from '.';

export default {
  title: 'CronPicker',
  component: CronPicker,
};

export const InteractiveCronPicker = (props: CronProps) => {
  // @ts-ignore
  const inputRef = useRef<Input>(null);
  const [value, setValue] = useState(props.value);
  const customSetValue = useCallback(
    (newValue: string) => {
      setValue(newValue);
      inputRef.current?.setValue(newValue);
    },
    [inputRef],
  );
  const [error, onError] = useState<CronError>();

  return (
    <div>
      <Input
        ref={inputRef}
        onBlur={event => {
          setValue(event.target.value);
        }}
        onChange={e => setValue(e.target.value || '')}
      />
      <Divider />
      <CronPicker
        {...props}
        value={value}
        setValue={customSetValue}
        onError={onError}
      />
      {error && <p style={{ marginTop: 20 }}>Error: {error.description}</p>}
    </div>
  );
};

InteractiveCronPicker.args = {
  clearButton: false,
  disabled: false,
  readOnly: false,
};

InteractiveCronPicker.argTypes = {
  value: {
    defaultValue: '30 5 * * *',
    table: {
      disable: true,
    },
  },
  theme: {
    table: {
      disable: true,
    },
  },
};

InteractiveCronPicker.story = {
  parameters: {
    knobs: {
      disable: true,
    },
  },
};
