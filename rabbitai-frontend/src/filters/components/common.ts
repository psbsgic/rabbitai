
import { styled } from '@rabbitai-ui/core';
import { Select } from 'src/common/components';
import { PluginFilterStylesProps } from './types';

export const Styles = styled.div<PluginFilterStylesProps>`
  height: ${({ height }) => height}px;
  width: ${({ width }) => width}px;
`;

export const StyledSelect = styled(Select)`
  width: 100%;
`;
