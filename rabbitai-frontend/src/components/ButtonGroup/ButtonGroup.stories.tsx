
import React from 'react';
import Button, { ButtonProps } from 'src/components/Button';
import { STYLES, SIZES } from 'src/components/Button/Button.stories';
import ButtonGroup from './index';

export default {
  title: 'ButtonGroup',
  component: ButtonGroup,
};

export const InteractiveButtonGroup = (args: ButtonProps) => (
  <>
    <ButtonGroup css={{ marginBottom: 40 }}>
      <Button {...args}>Button 1</Button>
    </ButtonGroup>
    <ButtonGroup css={{ marginBottom: 40 }}>
      <Button {...args}>Button 1</Button>
      <Button {...args}>Button 2</Button>
    </ButtonGroup>
    <ButtonGroup>
      <Button {...args}>Button 1</Button>
      <Button {...args}>Button 2</Button>
      <Button {...args}>Button 3</Button>
    </ButtonGroup>
  </>
);
InteractiveButtonGroup.args = {
  buttonStyle: 'tertiary',
  buttonSize: 'default',
};

InteractiveButtonGroup.argTypes = {
  buttonStyle: {
    name: STYLES.label,
    control: { type: 'select', options: STYLES.options },
  },
  buttonSize: {
    name: SIZES.label,
    control: { type: 'select', options: SIZES.options },
  },
};

InteractiveButtonGroup.story = {
  parameters: {
    actions: {
      disable: true,
    },
    knobs: {
      disable: true,
    },
  },
};
