import React, { useState } from 'react';
import SearchInput, { SearchInputProps } from '.';

export default {
  title: 'SearchInput',
  component: SearchInput,
};

export const InteractiveSearchInput = ({
  value,
  ...rest
}: SearchInputProps) => {
  const [currentValue, setCurrentValue] = useState(value);
  return (
    <div style={{ width: 230 }}>
      <SearchInput
        {...rest}
        value={currentValue}
        onChange={e => setCurrentValue(e.target.value)}
        onClear={() => setCurrentValue('')}
      />
    </div>
  );
};

InteractiveSearchInput.args = {
  value: 'Test',
  placeholder: 'Enter some text',
  name: 'search-input',
};

InteractiveSearchInput.argTypes = {
  onSubmit: { action: 'onSubmit' },
  onClear: { action: 'onClear' },
  onChange: { action: 'onChange' },
};

InteractiveSearchInput.story = {
  parameters: {
    knobs: {
      disable: true,
    },
  },
};
