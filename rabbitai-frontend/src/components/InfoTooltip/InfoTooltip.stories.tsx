
import React from 'react';
import InfoTooltip, { InfoTooltipProps } from 'src/components/InfoTooltip';

export default {
  title: 'InfoTooltip',
  component: InfoTooltip,
};

export const InteractiveInfoTooltip = (props: InfoTooltipProps) => {
  const styles = {
    padding: '100px 0 0 200px',
  };

  return (
    <div style={styles}>
      <InfoTooltip {...props} />
    </div>
  );
};

InteractiveInfoTooltip.args = {
  tooltip: 'This is the text that will display!',
};

InteractiveInfoTooltip.argTypes = {
  placement: {
    defaultValue: 'top',
    control: {
      type: 'select',
      options: [
        'bottom',
        'left',
        'right',
        'top',
        'topLeft',
        'topRight',
        'bottomLeft',
        'bottomRight',
        'leftTop',
        'leftBottom',
        'rightTop',
        'rightBottom',
      ],
    },
  },
  trigger: {
    defaultValue: 'hover',
    control: {
      type: 'select',
      options: ['hover', 'click'],
    },
  },
};

InteractiveInfoTooltip.story = {
  parameters: {
    knobs: {
      disable: true,
    },
  },
};
