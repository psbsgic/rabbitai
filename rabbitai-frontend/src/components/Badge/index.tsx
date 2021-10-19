import React from 'react';
import { styled } from '@superset-ui/core';
import { Badge as AntdBadge } from 'antd';
import { BadgeProps as AntdBadgeProps } from 'antd/lib/badge';

export interface BadgeProps extends AntdBadgeProps {
  textColor?: string;
}

const Badge = styled((
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  { textColor, ...props }: BadgeProps,
) => <AntdBadge {...props} />)`
  & > sup {
    padding: 0 ${({ theme }) => theme.gridUnit * 2}px;
    background: ${({ theme, color }) => color || theme.colors.primary.base};
    color: ${({ theme, textColor }) =>
      textColor || theme.colors.grayscale.light5};
  }
`;

export default Badge;
