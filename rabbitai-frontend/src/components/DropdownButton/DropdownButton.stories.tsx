
import React from 'react';
import { Menu } from 'src/common/components';
import { DropdownButton, DropdownButtonProps } from '.';

export default {
  title: 'DropdownButton',
};

const menu = (
  <Menu>
    <Menu.Item>1st menu item</Menu.Item>
    <Menu.Item>2nd menu item</Menu.Item>
    <Menu.Item>3rd menu item</Menu.Item>
  </Menu>
);

const PLACEMENTS = [
  'bottom',
  'bottomLeft',
  'bottomRight',
  'left',
  'leftBottom',
  'leftTop',
  'right',
  'rightBottom',
  'rightTop',
  'top',
  'topLeft',
  'topRight',
];

export const InteractiveDropdownButton = (args: DropdownButtonProps) => (
  <div style={{ margin: '50px 100px' }}>
    <DropdownButton {...args}>Hover</DropdownButton>
  </div>
);

InteractiveDropdownButton.args = {
  tooltip: 'Tooltip',
};

InteractiveDropdownButton.argTypes = {
  placement: {
    defaultValue: 'top',
    control: { type: 'select', options: PLACEMENTS },
  },
  overlay: {
    defaultValue: menu,
    table: {
      disable: true,
    },
  },
};

InteractiveDropdownButton.story = {
  parameters: {
    knobs: {
      disable: true,
    },
  },
};
