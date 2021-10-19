import React from 'react';
import { styled } from '@superset-ui/core';
import BaseSwitch, { SwitchProps } from 'antd/lib/switch';

const StyledSwitch = styled(BaseSwitch)`
  .ant-switch-checked {
    background-color: ${({ theme }) => theme.colors.primary.base};
  }
`;

export const Switch = (props: SwitchProps) => <StyledSwitch {...props} />;
export { SwitchProps };
