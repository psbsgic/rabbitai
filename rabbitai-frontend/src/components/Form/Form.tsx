import React from 'react';
import AntDForm, { FormProps } from 'antd/lib/form';
import { styled } from '@superset-ui/core';

const StyledForm = styled(AntDForm)`
  &.ant-form label {
    font-size: ${({ theme }) => theme.typography.sizes.s}px;
  }
  .ant-form-item {
    margin-bottom: ${({ theme }) => theme.gridUnit * 4}px;
  }
`;

export default function Form(props: FormProps) {
  return <StyledForm {...props} />;
}

export { FormProps };
