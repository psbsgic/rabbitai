import React from 'react';
import { useArgs } from '@storybook/client-api';
import Checkbox from '.';

export default {
  title: 'Checkbox',
  component: Checkbox,
};

const STATUSES = {
  checked: true,
  unchecked: false,
};

export const CheckboxGallery = () =>
  Object.keys(STATUSES).map(status => (
    <div style={{ marginBottom: '16px' }} key={status}>
      <Checkbox
        onChange={() => {}}
        checked={STATUSES[status]}
        style={{ marginRight: '8px' }}
      />
      {`I'm a${STATUSES[status] ? '' : 'n'} ${status} checkbox`}
    </div>
  ));

// eslint-disable-next-line no-unused-vars
export const InteractiveCheckbox = _args => {
  const [{ checked, style }, updateArgs] = useArgs();
  const toggleCheckbox = () => {
    updateArgs({ checked: !checked });
  };

  return (
    <>
      <Checkbox onChange={toggleCheckbox} checked={checked} style={style} />
      I'm an interactive checkbox
    </>
  );
};

InteractiveCheckbox.args = {
  checked: false,
  style: { marginRight: '8px' },
};
