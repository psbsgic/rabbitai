
import React, { ReactNode } from 'react';
import { Tooltip } from 'src/components/Tooltip';
import { styled } from '@rabbitai-ui/core';

export interface Props {
  children?: ReactNode;
  className?: string;
  onClick?: () => void;
  placement?:
    | 'bottom'
    | 'left'
    | 'right'
    | 'top'
    | 'topLeft'
    | 'topRight'
    | 'bottomLeft'
    | 'bottomRight'
    | 'leftTop'
    | 'leftBottom'
    | 'rightTop'
    | 'rightBottom';
  style?: object;
  tooltip?: string | null;
}

const StyledSpan = styled.span`
  color: ${({ theme }) => theme.colors.primary.dark1};
  &: hover {
    color: ${({ theme }) => theme.colors.primary.dark2};
  }
`;

const IconTooltip = ({
  children = null,
  className = '',
  onClick = () => undefined,
  placement = 'top',
  style = {},
  tooltip = null,
}: Props) => {
  const iconTooltip = (
    <StyledSpan
      onClick={onClick}
      style={style}
      className={`IconTooltip ${className}`}
    >
      {children}
    </StyledSpan>
  );
  if (tooltip) {
    return (
      <Tooltip
        id="tooltip"
        title={tooltip}
        placement={placement}
        mouseEnterDelay={0.3}
        mouseLeaveDelay={0.15}
      >
        {iconTooltip}
      </Tooltip>
    );
  }
  return iconTooltip;
};

export { IconTooltip };
