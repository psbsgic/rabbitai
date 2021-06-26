
import React from 'react';
import cx from 'classnames';
import { styled, useTheme } from '@rabbitai-ui/core';
import { Dropdown, Menu } from 'src/common/components';
import Icon from 'src/components/Icon';

export interface OptionProps {
  value: string;
  label: string;
  className?: string;
}

export type OnChangeHandler = (key: React.Key) => void;
export type RenderElementHandler = (option: OptionProps) => JSX.Element;

export interface PopoverDropdownProps {
  id: string;
  options: OptionProps[];
  onChange: OnChangeHandler;
  value: string;
  renderButton?: RenderElementHandler;
  renderOption?: RenderElementHandler;
}

interface HandleSelectProps {
  key: React.Key;
}

const MenuItem = styled(Menu.Item)`
  &.ant-menu-item {
    height: auto;
    line-height: 1.4;

    padding-top: ${({ theme }) => theme.gridUnit}px;
    padding-bottom: ${({ theme }) => theme.gridUnit}px;

    margin-top: 0;
    margin-bottom: 0;

    &:not(:last-child) {
      margin-bottom: 0;
    }

    &:hover {
      background: ${({ theme }) => theme.colors.grayscale.light3};
    }

    &.active {
      font-weight: ${({ theme }) => theme.typography.weights.bold};
      background: ${({ theme }) => theme.colors.grayscale.light2};
    }
  }

  &.ant-menu-item-selected {
    color: unset;
  }
`;

const PopoverDropdown = (props: PopoverDropdownProps) => {
  const {
    value,
    options,
    onChange,
    renderButton = (option: OptionProps) => option.label,
    renderOption = (option: OptionProps) => (
      <div className={option.className}>{option.label}</div>
    ),
  } = props;

  const theme = useTheme();
  const selected = options.find(opt => opt.value === value);
  return (
    <Dropdown
      trigger={['click']}
      overlayStyle={{ zIndex: theme.zIndex.max }}
      overlay={
        <Menu onClick={({ key }: HandleSelectProps) => onChange(key)}>
          {options.map(option => (
            <MenuItem
              id="menu-item"
              key={option.value}
              className={cx('dropdown-item', {
                active: option.value === value,
              })}
            >
              {renderOption(option)}
            </MenuItem>
          ))}
        </Menu>
      }
    >
      <div role="button" css={{ display: 'flex', alignItems: 'center' }}>
        {selected && renderButton(selected)}
        <Icon name="caret-down" css={{ marginTop: theme.gridUnit }} />
      </div>
    </Dropdown>
  );
};

export default PopoverDropdown;
