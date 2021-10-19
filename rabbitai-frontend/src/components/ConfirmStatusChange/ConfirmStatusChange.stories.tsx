import React from 'react';
import Button from 'src/components/Button';
import ConfirmStatusChange, { ConfirmStatusChangeProps, Callback } from '.';

export default {
  title: 'ConfirmStatusChange',
};

export const InteractiveConfirmStatusChange = (
  args: ConfirmStatusChangeProps,
) => <ConfirmStatusChange {...args} />;

InteractiveConfirmStatusChange.args = {
  title: 'Delete confirmation',
  description: 'Are you sure you want to delete?',
  children: (showConfirm: Callback) => (
    <Button onClick={() => showConfirm()}>DELETE</Button>
  ),
};

InteractiveConfirmStatusChange.argTypes = {
  onConfirm: { action: 'onConfirm' },
};

InteractiveConfirmStatusChange.story = {
  parameters: {
    knobs: {
      disable: true,
    },
  },
};
