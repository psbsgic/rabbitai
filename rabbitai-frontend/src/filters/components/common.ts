import { styled } from '@superset-ui/core';
import { PluginFilterStylesProps } from './types';
import FormItem from '../../components/Form/FormItem';

export const FilterPluginStyle = styled.div<PluginFilterStylesProps>`
  min-height: ${({ height }) => height}px;
  width: ${({ width }) => width}px;
`;

export const StyledFormItem = styled(FormItem)`
  &.ant-row.ant-form-item {
    margin: 0;
  }
`;

export const StatusMessage = styled.div<{
  status?: 'error' | 'warning' | 'info';
}>`
  color: ${({ theme, status = 'error' }) => theme.colors[status]?.base};
`;
