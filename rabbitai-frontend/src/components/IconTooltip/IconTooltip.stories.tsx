import React from 'react';
import Icons from 'src/components/Icons';
import { IconTooltip, Props } from '.';

export default {
  title: 'IconTooltip',
};

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

export const InteractiveIconTooltip = (args: Props) => (
  <div css={{ margin: '40px 70px' }}>
    <IconTooltip {...args}>
      <Icons.Info />
    </IconTooltip>
  </div>
);

InteractiveIconTooltip.args = {
  tooltip: 'Tooltip',
};

InteractiveIconTooltip.argTypes = {
  placement: {
    defaultValue: 'top',
    control: { type: 'select', options: PLACEMENTS },
  },
};

InteractiveIconTooltip.story = {
  parameters: {
    knobs: {
      disable: true,
    },
  },
};
