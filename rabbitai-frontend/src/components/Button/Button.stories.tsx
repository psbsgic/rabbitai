
import React from 'react';
import Button, { ButtonProps } from './index';

type ButtonStyle = Pick<ButtonProps, 'buttonStyle'>;
type ButtonStyleValue = ButtonStyle[keyof ButtonStyle];
type ButtonSize = Pick<ButtonProps, 'buttonSize'>;
type ButtonSizeValue = ButtonSize[keyof ButtonSize];

export default {
  title: 'Button',
  component: Button,
  includeStories: ['ButtonGallery', 'InteractiveButton'],
};

const buttonStyles: ButtonStyleValue[] = [
  'primary',
  'secondary',
  'tertiary',
  'dashed',
  'danger',
  'warning',
  'success',
  'link',
  'default',
];

const buttonSizes: ButtonSizeValue[] = ['xsmall', 'small', 'default'];

export const STYLES = {
  label: 'styles',
  options: buttonStyles,
  defaultValue: undefined,
};

export const SIZES = {
  label: 'sizes',
  options: buttonSizes,
  defaultValue: undefined,
};

const TARGETS = {
  label: 'target',
  options: {
    blank: '_blank',
    none: null,
  },
  defaultValue: null,
};

const HREFS = {
  label: 'href',
  options: {
    rabbitai: 'https://rabbitai.apache.org/',
    none: null,
  },
  defaultValue: null,
};

export const ButtonGallery = () => (
  <>
    {SIZES.options.map(size => (
      <div key={size} style={{ marginBottom: 40 }}>
        <h4>{size}</h4>
        {Object.values(STYLES.options).map(style => (
          <Button
            buttonStyle={style}
            buttonSize={size}
            onClick={() => true}
            key={`${style}_${size}`}
            style={{ marginRight: 20, marginBottom: 10 }}
          >
            {style}
          </Button>
        ))}
      </div>
    ))}
  </>
);

ButtonGallery.story = {
  parameters: {
    actions: {
      disable: true,
    },
    controls: {
      disable: true,
    },
    knobs: {
      disable: true,
    },
  },
};

export const InteractiveButton = (args: ButtonProps & { label: string }) => {
  const { label, ...btnArgs } = args;
  return <Button {...btnArgs}>{label}</Button>;
};

InteractiveButton.story = {
  parameters: {
    knobs: {
      disable: true,
    },
  },
};

InteractiveButton.args = {
  buttonStyle: 'default',
  buttonSize: 'default',
  label: 'Button!',
};

InteractiveButton.argTypes = {
  target: {
    name: TARGETS.label,
    control: { type: 'select', options: Object.values(TARGETS.options) },
  },
  href: {
    name: HREFS.label,
    control: { type: 'select', options: Object.values(HREFS.options) },
  },
  onClick: { action: 'clicked' },
};
