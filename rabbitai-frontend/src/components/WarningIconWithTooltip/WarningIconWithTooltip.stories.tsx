
import React from 'react';
import WarningIconWithTooltip, { WarningIconWithTooltipProps } from '.';

export default {
  title: 'WarningIconWithTooltip',
  component: WarningIconWithTooltip,
};

export const InteractiveWarningIcon = (args: WarningIconWithTooltipProps) => (
  <div css={{ margin: 40 }}>
    <WarningIconWithTooltip {...args} />
  </div>
);

InteractiveWarningIcon.args = {
  warningMarkdown: 'Markdown example',
  size: 20,
};

InteractiveWarningIcon.story = {
  parameters: {
    knobs: {
      disable: true,
    },
  },
};
