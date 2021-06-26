
import React from 'react';
import ProgressBar, { ProgressBarProps } from '.';

export default {
  title: 'ProgressBar',
  component: ProgressBar,
};

export const InteractiveProgressBar = (args: ProgressBarProps) => (
  <ProgressBar {...args} />
);

InteractiveProgressBar.args = {
  striped: true,
  percent: 90,
  showInfo: true,
  status: 'normal',
  strokeColor: '#FF0000',
  trailColor: '#000',
  strokeLinecap: 'round',
  type: 'line',
};

InteractiveProgressBar.argTypes = {
  status: {
    control: {
      type: 'select',
      options: ['normal', 'success', 'exception', 'active'],
    },
  },
  strokeLinecap: {
    control: {
      type: 'select',
      options: ['round', 'square'],
    },
  },
  type: {
    control: {
      type: 'select',
      options: ['line', 'circle', 'dashboard'],
    },
  },
};
