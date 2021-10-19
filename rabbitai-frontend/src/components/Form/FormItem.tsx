import Form from 'antd/lib/form';
import { styled } from '@superset-ui/core';

const StyledItem = styled(Form.Item)`
  ${({ theme }) => `
    .ant-form-item-label {
      padding-bottom: ${theme.gridUnit}px;
      & > label {
        text-transform: uppercase;
        font-size: ${theme.typography.sizes.s}px;
        color: ${theme.colors.grayscale.base};

        &.ant-form-item-required:not(.ant-form-item-required-mark-optional) {
          &::before {
            display: none;
          }
          &::after {
            display: inline-block;
            color: ${theme.colors.error.base};
            font-size: ${theme.typography.sizes.s}px;
            content: '*';
          }
        }
      }
    }
  `}
`;

export default StyledItem;
