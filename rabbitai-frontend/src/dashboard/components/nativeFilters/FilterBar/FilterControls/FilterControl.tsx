import React from 'react';
import { styled } from '@superset-ui/core';
import { Form, FormItem } from 'src/components/Form';
import FilterValue from './FilterValue';
import { FilterProps } from './types';
import { checkIsMissingRequiredValue } from '../utils';

const StyledIcon = styled.div`
  position: absolute;
  right: 0;
`;

const StyledFilterControlTitle = styled.h4`
  font-size: ${({ theme }) => theme.typography.sizes.s}px;
  color: ${({ theme }) => theme.colors.grayscale.dark1};
  margin: 0;
  overflow-wrap: break-word;
`;

const StyledFilterControlTitleBox = styled.div`
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  margin-bottom: ${({ theme }) => theme.gridUnit}px;
`;

const StyledFilterControlContainer = styled(Form)`
  width: 100%;
  && .ant-form-item-label > label {
    text-transform: none;
    width: 100%;
    padding-right: ${({ theme }) => theme.gridUnit * 11}px;
  }
`;

const FilterControl: React.FC<FilterProps> = ({
  dataMaskSelected,
  filter,
  icon,
  onFilterSelectionChange,
  directPathToChild,
  inView,
}) => {
  const { name = '<undefined>' } = filter;

  const isMissingRequiredValue = checkIsMissingRequiredValue(
    filter,
    filter.dataMask?.filterState,
  );

  return (
    <StyledFilterControlContainer layout="vertical">
      <FormItem
        label={
          <StyledFilterControlTitleBox>
            <StyledFilterControlTitle data-test="filter-control-name">
              {name}
            </StyledFilterControlTitle>
            <StyledIcon data-test="filter-icon">{icon}</StyledIcon>
          </StyledFilterControlTitleBox>
        }
        required={filter?.controlValues?.enableEmptyFilter}
        validateStatus={isMissingRequiredValue ? 'error' : undefined}
      >
        <FilterValue
          dataMaskSelected={dataMaskSelected}
          filter={filter}
          directPathToChild={directPathToChild}
          onFilterSelectionChange={onFilterSelectionChange}
          inView={inView}
        />
      </FormItem>
    </StyledFilterControlContainer>
  );
};

export default FilterControl;
