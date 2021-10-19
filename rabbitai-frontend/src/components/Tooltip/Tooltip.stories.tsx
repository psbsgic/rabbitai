import React from 'react';
import Button from 'src/components/Button';
import { TooltipProps, TooltipPlacement } from 'antd/lib/tooltip';
import { Tooltip } from './index';

export default {
  title: 'Tooltip',
  component: Tooltip,
};

const PLACEMENTS: TooltipPlacement[] = [
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

const TRIGGERS = ['hover', 'focus', 'click', 'contextMenu'];

export const InteractiveTooltip = (args: TooltipProps) => (
  <Tooltip {...args}>
    <Button style={{ margin: '50px 100px' }}>Hover me</Button>
  </Tooltip>
);

InteractiveTooltip.story = {
  parameters: {
    knobs: {
      disable: true,
    },
  },
};

InteractiveTooltip.args = {
  title: 'Simple tooltip text',
  mouseEnterDelay: 0.1,
  mouseLeaveDelay: 0.1,
};

InteractiveTooltip.argTypes = {
  placement: {
    defaultValue: 'top',
    control: { type: 'select', options: PLACEMENTS },
  },
  trigger: {
    defaultValue: 'hover',
    control: { type: 'select', options: TRIGGERS },
  },
  color: { control: { type: 'color' } },
  onVisibleChange: { action: 'onVisibleChange' },
};
