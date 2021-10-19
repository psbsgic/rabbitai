import React from 'react';
import { Dropdown as AntdDropdown } from 'antd';
import { styled } from '@superset-ui/core';

const MenuDots = styled.div`
  width: ${({ theme }) => theme.gridUnit * 0.75}px;
  height: ${({ theme }) => theme.gridUnit * 0.75}px;
  border-radius: 50%;
  background-color: ${({ theme }) => theme.colors.grayscale.light1};

  font-weight: ${({ theme }) => theme.typography.weights.normal};
  display: inline-flex;
  position: relative;

  &:hover {
    background-color: ${({ theme }) => theme.colors.primary.base};

    &::before,
    &::after {
      background-color: ${({ theme }) => theme.colors.primary.base};
    }
  }

  &::before,
  &::after {
    position: absolute;
    content: ' ';
    width: ${({ theme }) => theme.gridUnit * 0.75}px;
    height: ${({ theme }) => theme.gridUnit * 0.75}px;
    border-radius: 50%;
    background-color: ${({ theme }) => theme.colors.grayscale.light1};
  }

  &::before {
    top: ${({ theme }) => theme.gridUnit}px;
  }

  &::after {
    bottom: ${({ theme }) => theme.gridUnit}px;
  }
`;

const MenuDotsWrapper = styled.div`
  display: flex;
  align-items: center;
  padding: ${({ theme }) => theme.gridUnit * 2}px;
  padding-left: ${({ theme }) => theme.gridUnit}px;
`;

export interface DropdownProps {
  overlay: React.ReactElement;
}

export const Dropdown = ({ overlay, ...rest }: DropdownProps) => (
  <AntdDropdown overlay={overlay} {...rest}>
    <MenuDotsWrapper>
      <MenuDots />
    </MenuDotsWrapper>
  </AntdDropdown>
);
