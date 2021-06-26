
import React from 'react';
import Slider, { SliderSingleProps } from '.';

export default {
  title: 'Slider',
  component: Slider,
};

export const InteractiveSlider = (args: SliderSingleProps) => (
  <Slider {...args} style={{ width: 400, height: 400 }} />
);

InteractiveSlider.args = {
  min: 0,
  max: 100,
  defaultValue: 70,
  step: 1,
};

InteractiveSlider.argTypes = {
  onChange: { action: 'onChange' },
  disabled: {
    control: { type: 'boolean' },
  },
  reverse: {
    control: { type: 'boolean' },
  },
  vertical: {
    control: { type: 'boolean' },
  },
};

InteractiveSlider.story = {
  parameters: {
    knobs: {
      disable: true,
    },
  },
};
