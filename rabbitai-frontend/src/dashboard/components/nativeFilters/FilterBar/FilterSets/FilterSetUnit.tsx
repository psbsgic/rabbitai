import { Typography, Dropdown, Menu } from 'src/common/components';
import React, { FC } from 'react';
import { FilterSet } from 'src/dashboard/reducers/types';
import { DataMaskState } from 'src/dataMask/types';
import { CheckOutlined, EllipsisOutlined } from '@ant-design/icons';
import { HandlerFunction, styled, supersetTheme, t } from '@superset-ui/core';
import Button from 'src/components/Button';
import { Tooltip } from 'src/components/Tooltip';
import FiltersHeader from './FiltersHeader';
import { getFilterBarTestId } from '..';

const HeaderButton = styled(Button)`
  padding: 0;
`;

const TitleText = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const IconsBlock = styled.div`
  display: flex;
  justify-content: flex-end;
  align-items: center;
  & > *,
  & > button.rabbitai-button {
    ${({ theme }) => `margin-left: ${theme.gridUnit * 2}px`};
  }
`;

export type FilterSetUnitProps = {
  editMode?: boolean;
  isApplied?: boolean;
  filterSet?: FilterSet;
  filterSetName?: string;
  dataMaskSelected?: DataMaskState;
  setFilterSetName?: (name: string) => void;
  onDelete?: HandlerFunction;
  onEdit?: HandlerFunction;
  onRebuild?: HandlerFunction;
};

const FilterSetUnit: FC<FilterSetUnitProps> = ({
  editMode,
  setFilterSetName,
  onDelete,
  onEdit,
  filterSetName,
  dataMaskSelected,
  filterSet,
  isApplied,
  onRebuild,
}) => {
  const menu = (
    <Menu>
      <Menu.Item onClick={onEdit}>{t('Edit')}</Menu.Item>
      <Menu.Item onClick={onRebuild}>
        <Tooltip placement="right" title={t('Remove invalid filters')}>
          {t('Rebuild')}
        </Tooltip>
      </Menu.Item>
      <Menu.Item onClick={onDelete} danger>
        {t('Delete')}
      </Menu.Item>
    </Menu>
  );

  return (
    <>
      <TitleText>
        <Typography.Text
          strong
          editable={{
            editing: editMode,
            icon: <span />,
            onChange: setFilterSetName,
          }}
        >
          {filterSet?.name ?? filterSetName}
        </Typography.Text>
        <IconsBlock>
          {isApplied && (
            <CheckOutlined
              style={{ color: supersetTheme.colors.success.base }}
            />
          )}
          {onDelete && (
            <Dropdown
              overlay={menu}
              placement="bottomRight"
              trigger={['click']}
            >
              <HeaderButton
                onClick={e => {
                  e.stopPropagation();
                  e.preventDefault();
                }}
                {...getFilterBarTestId('filter-set-menu-button')}
                buttonStyle="link"
                buttonSize="xsmall"
              >
                <EllipsisOutlined />
              </HeaderButton>
            </Dropdown>
          )}
        </IconsBlock>
      </TitleText>
      <FiltersHeader
        filterSet={filterSet}
        dataMask={filterSet?.dataMask ?? dataMaskSelected}
      />
    </>
  );
};

export default FilterSetUnit;
