import React from 'react';
import IconButton, { IconButtonProps } from '.';

export default {
  title: 'IconButton',
  component: IconButton,
};

export const InteractiveIconButton = (args: IconButtonProps) => (
  <IconButton
    buttonText={args.buttonText}
    altText={args.altText}
    icon={args.icon}
    href={args.href}
    target={args.target}
    htmlType={args.htmlType}
  />
);

InteractiveIconButton.args = {
  buttonText: 'This is the IconButton text',
  altText: 'This is an example of non-default alt text',
  href: 'https://preset.io/',
  target: '_blank',
};

InteractiveIconButton.argTypes = {
  icon: {
    defaultValue: '/images/icons/sql.svg',
    control: {
      type: 'select',
      options: [
        '/images/icons/sql.svg',
        '/images/icons/server.svg',
        '/images/icons/image.svg',
        'Click to see example alt text',
      ],
    },
  },
};
