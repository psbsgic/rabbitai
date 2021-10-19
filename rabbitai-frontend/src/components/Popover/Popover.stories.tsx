import Button from 'src/components/Button';
import { PopoverProps } from 'antd/lib/popover';
import React from 'react';
import Popover from '.';

export default {
  title: 'Popover',
  component: Popover,
};

export const InteractivePopover = (args: PopoverProps) => (
  <Popover {...args}>
    <Button
      style={{
        display: 'block',
        margin: '80px auto',
      }}
    >
      I am a button
    </Button>
  </Popover>
);

const PLACEMENTS = {
  label: 'placement',
  options: [
    'topLeft',
    'top',
    'topRight',
    'leftTop',
    'left',
    'leftBottom',
    'rightTop',
    'right',
    'rightBottom',
    'bottomLeft',
    'bottom',
    'bottomRight',
  ],
  defaultValue: null,
};

const TRIGGERS = {
  label: 'trigger',
  options: ['hover', 'click', 'focus'],
  defaultValue: null,
};

InteractivePopover.args = {
  content: 'Popover sample content',
  title: 'Popover title',
};

InteractivePopover.argTypes = {
  placement: {
    name: PLACEMENTS.label,
    control: { type: 'select', options: PLACEMENTS.options },
  },
  trigger: {
    name: TRIGGERS.label,
    control: { type: 'select', options: TRIGGERS.options },
  },
};
