import React from 'react';
import { SupersetTheme } from '@superset-ui/core';
import AntdCard, { CardProps as AntdCardProps } from 'antd/lib/card';

export interface CardProps extends AntdCardProps {
  padded?: boolean;
}

const Card = ({ padded, ...props }: CardProps) => (
  <AntdCard
    {...props}
    css={(theme: SupersetTheme) => ({
      backgroundColor: theme.colors.grayscale.light4,
      borderRadius: theme.borderRadius,
      '.ant-card-body': {
        padding: padded ? theme.gridUnit * 4 : theme.gridUnit,
      },
    })}
  />
);

export default Card;
