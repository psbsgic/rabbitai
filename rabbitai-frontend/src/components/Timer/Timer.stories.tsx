import React from 'react';
import moment from 'moment';
import Timer, { TimerProps } from './index';

export default {
  title: 'Timer',
  component: Timer,
};

export const InteractiveTimer = (args: TimerProps) => <Timer {...args} />;

InteractiveTimer.args = {
  isRunning: false,
};

InteractiveTimer.argTypes = {
  startTime: {
    defaultValue: moment().utc().valueOf(),
    table: {
      disable: true,
    },
  },
  endTime: {
    table: {
      disable: true,
    },
  },
  status: {
    control: {
      type: 'select',
      options: [
        'success',
        'warning',
        'danger',
        'info',
        'default',
        'primary',
        'secondary',
      ],
    },
  },
};

InteractiveTimer.story = {
  parameters: {
    actions: {
      disabled: true,
    },
    knobs: {
      disabled: true,
    },
  },
};
