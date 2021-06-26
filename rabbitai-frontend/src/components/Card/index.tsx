
import React from 'react';
import { RabbitaiTheme } from '@rabbitai-ui/core';
import AntdCard, { CardProps as AntdCardProps } from 'antd/lib/card';

export interface CardProps extends AntdCardProps {
  padded?: boolean;
}

const Card = ({ padded, ...props }: CardProps) => (
  <AntdCard
    {...props}
    css={(theme: RabbitaiTheme) => ({
      backgroundColor: theme.colors.grayscale.light4,
      borderRadius: theme.borderRadius,
      '.ant-card-body': {
        padding: padded ? theme.gridUnit * 4 : theme.gridUnit,
      },
    })}
  />
);

export default Card;
