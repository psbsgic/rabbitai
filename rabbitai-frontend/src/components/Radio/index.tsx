import { styled } from '@superset-ui/core';
import { Radio as AntdRadio } from 'antd';

const StyledRadio = styled(AntdRadio)`
  .ant-radio-inner {
    top: -1px;
    left: 2px;
    width: ${({ theme }) => theme.gridUnit * 4}px;
    height: ${({ theme }) => theme.gridUnit * 4}px;
    border-width: 2px;
    border-color: ${({ theme }) => theme.colors.grayscale.light2};
  }

  .ant-radio.ant-radio-checked {
    .ant-radio-inner {
      border-width: ${({ theme }) => theme.gridUnit + 1}px;
      border-color: ${({ theme }) => theme.colors.primary.base};
    }

    .ant-radio-inner::after {
      background-color: ${({ theme }) => theme.colors.grayscale.light5};
      top: 0;
      left: 0;
      width: ${({ theme }) => theme.gridUnit + 2}px;
      height: ${({ theme }) => theme.gridUnit + 2}px;
    }
  }

  .ant-radio:hover,
  .ant-radio:focus {
    .ant-radio-inner {
      border-color: ${({ theme }) => theme.colors.primary.dark1};
    }
  }
`;
const StyledGroup = styled(AntdRadio.Group)`
  font-size: inherit;
`;

export const Radio = Object.assign(StyledRadio, {
  Group: StyledGroup,
});
