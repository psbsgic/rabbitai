
import { t, styled } from '@rabbitai-ui/core';
import React, { FC } from 'react';
import Button from 'src/components/Button';
import { Tooltip } from 'src/components/Tooltip';
import { APPLY_FILTERS_HINT } from './utils';
import { useFilterSetNameDuplicated } from './state';
import { getFilterBarTestId } from '..';

export type FooterProps = {
  filterSetName: string;
  disabled: boolean;
  editMode: boolean;
  onCancel: () => void;
  onEdit: () => void;
  onCreate: () => void;
};

const ActionButton = styled.div<{ disabled: boolean }>`
  display: flex;
  & button {
    ${({ disabled }) => `pointer-events: ${disabled ? 'none' : 'all'}`};
    flex: 1;
  }
`;

export const ActionButtons = styled.div`
  display: grid;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  grid-gap: 10px;
  grid-template-columns: 1fr 1fr;
`;

const Footer: FC<FooterProps> = ({
  onCancel,
  editMode,
  onEdit,
  onCreate,
  disabled,
  filterSetName,
}) => {
  const isFilterSetNameDuplicated = useFilterSetNameDuplicated(filterSetName);

  const isCreateDisabled =
    !filterSetName || isFilterSetNameDuplicated || disabled;

  return (
    <>
      {editMode ? (
        <ActionButtons>
          <Button
            buttonStyle="tertiary"
            buttonSize="small"
            onClick={onCancel}
            data-test="filter-set-cancel-button"
          >
            {t('Cancel')}
          </Button>
          <Tooltip
            placement="right"
            title={
              (!filterSetName && t('Please filter set name')) ||
              (isFilterSetNameDuplicated &&
                t('Filter set with this name already exists')) ||
              (disabled && APPLY_FILTERS_HINT)
            }
          >
            <ActionButton disabled={isCreateDisabled}>
              <Button
                disabled={isCreateDisabled}
                buttonStyle="primary"
                htmlType="submit"
                buttonSize="small"
                onClick={onCreate}
                {...getFilterBarTestId('create-filter-set-button')}
              >
                {t('Create')}
              </Button>
            </ActionButton>
          </Tooltip>
        </ActionButtons>
      ) : (
        <Tooltip placement="bottom" title={disabled && APPLY_FILTERS_HINT}>
          <ActionButton disabled={disabled}>
            <Button
              disabled={disabled}
              buttonStyle="tertiary"
              buttonSize="small"
              onClick={onEdit}
              {...getFilterBarTestId('new-filter-set-button')}
            >
              {t('Create new filter set')}
            </Button>
          </ActionButton>
        </Tooltip>
      )}
    </>
  );
};

export default Footer;
