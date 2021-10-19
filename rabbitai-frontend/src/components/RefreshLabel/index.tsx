import React, { MouseEventHandler } from 'react';
import { SupersetTheme } from '@superset-ui/core';
import { Tooltip } from 'src/components/Tooltip';
import Icons, { IconType } from 'src/components/Icons';

export interface RefreshLabelProps {
  onClick: MouseEventHandler<HTMLSpanElement>;
  tooltipContent: string;
}

const RefreshLabel = ({ onClick, tooltipContent }: RefreshLabelProps) => {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const IconWithoutRef = React.forwardRef((props: IconType, ref: any) => (
    <Icons.Refresh {...props} />
  ));

  return (
    <Tooltip title={tooltipContent}>
      <IconWithoutRef
        role="button"
        onClick={onClick}
        css={(theme: SupersetTheme) => ({
          cursor: 'pointer',
          color: theme.colors.grayscale.base,
          '&:hover': { color: theme.colors.primary.base },
        })}
      />
    </Tooltip>
  );
};

export default RefreshLabel;
