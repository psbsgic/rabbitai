
import React from 'react';
import RefreshLabel, { RefreshLabelProps } from '.';

export default {
  title: 'RefreshLabel',
};

export const InteractiveRefreshLabel = (args: RefreshLabelProps) => (
  <RefreshLabel {...args} />
);

InteractiveRefreshLabel.args = {
  tooltipContent: 'Tooltip',
};

InteractiveRefreshLabel.argTypes = {
  onClick: { action: 'onClick' },
};

InteractiveRefreshLabel.story = {
  parameters: {
    knobs: {
      disable: true,
    },
  },
};
