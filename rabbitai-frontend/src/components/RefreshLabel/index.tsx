
import React, { MouseEventHandler } from 'react';
import { RabbitaiTheme } from '@rabbitai-ui/core';
import { Tooltip } from 'src/components/Tooltip';
import Icon, { IconProps } from 'src/components/Icon';

export interface RefreshLabelProps {
  onClick: MouseEventHandler<SVGSVGElement>;
  tooltipContent: string;
}

const RefreshLabel = ({ onClick, tooltipContent }: RefreshLabelProps) => {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const IconWithoutRef = React.forwardRef((props: IconProps, ref: any) => (
    <Icon {...props} />
  ));

  return (
    <Tooltip title={tooltipContent}>
      <IconWithoutRef
        role="button"
        onClick={onClick}
        name="refresh"
        css={(theme: RabbitaiTheme) => ({
          cursor: 'pointer',
          color: theme.colors.grayscale.base,
          '&:hover': { color: theme.colors.primary.base },
        })}
      />
    </Tooltip>
  );
};

export default RefreshLabel;
