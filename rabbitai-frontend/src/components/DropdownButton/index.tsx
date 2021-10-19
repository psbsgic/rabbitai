import React, { ReactNode } from 'react';
import { Dropdown as AntdDropdown, Tooltip } from 'src/common/components';
import { styled } from '@superset-ui/core';
import kebabCase from 'lodash/kebabCase';

const StyledDropdownButton = styled.div`
  .ant-btn-group {
    button.ant-btn {
      background-color: ${({ theme }) => theme.colors.primary.dark1};
      border-color: transparent;
      color: ${({ theme }) => theme.colors.grayscale.light5};
      font-size: 12px;
      line-height: 13px;
      outline: none;
      text-transform: uppercase;
      &:first-of-type {
        border-radius: ${({ theme }) =>
          `${theme.gridUnit}px 0 0 ${theme.gridUnit}px`};
        margin: 0;
        width: 120px;
      }

      &:disabled {
        background-color: ${({ theme }) => theme.colors.grayscale.light2};
        color: ${({ theme }) => theme.colors.grayscale.base};
      }
      &:nth-child(2) {
        margin: 0;
        border-radius: ${({ theme }) =>
          `0 ${theme.gridUnit}px ${theme.gridUnit}px 0`};
        width: ${({ theme }) => theme.gridUnit * 9}px;
        &:before,
        &:hover:before {
          border-left: 1px solid ${({ theme }) => theme.colors.grayscale.light5};
          content: '';
          display: block;
          height: 23px;
          margin: 0;
          position: absolute;
          top: ${({ theme }) => theme.gridUnit * 0.75}px;
          width: ${({ theme }) => theme.gridUnit * 0.25}px;
        }

        &:disabled:before {
          border-left: 1px solid ${({ theme }) => theme.colors.grayscale.base};
        }
      }
    }
  }
`;

export interface DropdownButtonProps {
  overlay: React.ReactElement;
  tooltip?: string;
  placement?: 'topLeft' | 'topRight' | 'bottomLeft' | 'bottomRight';
  buttonsRender?: ((buttons: ReactNode[]) => ReactNode[]) | undefined;
}

export const DropdownButton = ({
  overlay,
  tooltip,
  placement,
  ...rest
}: DropdownButtonProps) => {
  const buildButton = (
    props: {
      buttonsRender?: DropdownButtonProps['buttonsRender'];
    } = {},
  ) => (
    <StyledDropdownButton>
      <AntdDropdown.Button overlay={overlay} {...rest} {...props} />
    </StyledDropdownButton>
  );
  if (tooltip) {
    return buildButton({
      buttonsRender: ([leftButton, rightButton]) => [
        <Tooltip
          placement={placement}
          id={`${kebabCase(tooltip)}-tooltip`}
          title={tooltip}
        >
          {leftButton}
        </Tooltip>,
        rightButton,
      ],
    });
  }
  return buildButton();
};
