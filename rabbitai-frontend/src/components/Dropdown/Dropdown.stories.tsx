import React from 'react';
import { Menu } from 'src/common/components';
import { Dropdown, DropdownProps } from '.';

export default {
  title: 'Dropdown',
};

const menu = (
  <Menu>
    <Menu.Item>1st menu item</Menu.Item>
    <Menu.Item>2nd menu item</Menu.Item>
    <Menu.Item>3rd menu item</Menu.Item>
  </Menu>
);

const customOverlay = (
  <div
    style={{
      textAlign: 'center',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      backgroundColor: 'yellow',
      width: 100,
      height: 100,
    }}
  >
    Custom overlay
  </div>
);

export const InteractiveDropdown = ({
  overlayType,
  ...rest
}: DropdownProps & { overlayType: string }) => (
  <Dropdown
    {...rest}
    overlay={overlayType === 'custom' ? customOverlay : menu}
  />
);

InteractiveDropdown.argTypes = {
  overlayType: {
    defaultValue: 'menu',
    control: { type: 'radio', options: ['menu', 'custom'] },
  },
};

InteractiveDropdown.story = {
  parameters: {
    knobs: {
      disable: true,
    },
  },
};
