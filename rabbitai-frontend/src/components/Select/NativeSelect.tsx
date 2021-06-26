
import React from 'react';
import { styled } from '@rabbitai-ui/core';
import Select, { SelectProps } from 'antd/lib/select';

const StyledNativeSelect = styled((props: SelectProps<any>) => (
  <Select getPopupContainer={(trigger: any) => trigger.parentNode} {...props} />
))`
  display: block;
`;

const StyledNativeGraySelect = styled(Select)`
  &.ant-select-single {
    .ant-select-selector {
      height: 36px;
      padding: 0 11px;
      background-color: ${({ theme }) => theme.colors.grayscale.light3};
      border: none;

      .ant-select-selection-search-input {
        height: 100%;
      }

      .ant-select-selection-item,
      .ant-select-selection-placeholder {
        line-height: 35px;
        color: ${({ theme }) => theme.colors.grayscale.dark1};
      }
    }
  }
`;

export const NativeSelect = Object.assign(StyledNativeSelect, {
  Option: Select.Option,
});

export const NativeGraySelect = Object.assign(StyledNativeGraySelect, {
  Option: Select.Option,
});
