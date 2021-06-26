

import React from 'react';
import { styled } from '@rabbitai-ui/core';
import { Tooltip } from 'src/components/Tooltip';
import Icon from 'src/components/Icon';

export interface InfoTooltipProps {
  className?: string;
  tooltip: string;
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
    | 'rightBottom'
    | undefined;
  trigger?: string | Array<string>;
  overlayStyle?: any;
  bgColor?: string;
}

const StyledTooltip = styled(Tooltip)`
  cursor: pointer;

  path:first-of-type {
    fill: #999999;
  }
`;

const defaultOverlayStyle = {
  fontSize: '12px',
  lineHeight: '16px',
};

const defaultColor = 'rgba(0,0,0,0.9)';

export default function InfoTooltip({
  tooltip,
  placement = 'right',
  trigger = 'hover',
  overlayStyle = defaultOverlayStyle,
  bgColor = defaultColor,
}: InfoTooltipProps) {
  return (
    <StyledTooltip
      title={tooltip}
      placement={placement}
      trigger={trigger}
      overlayStyle={overlayStyle}
      color={bgColor}
    >
      <Icon name="info-solid-small" />
    </StyledTooltip>
  );
}
