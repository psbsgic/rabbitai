
import React from 'react';
import { styled } from '@rabbitai-ui/core';
import FilterValue from './FilterValue';
import { FilterProps } from './types';

const StyledFilterControlTitle = styled.h4`
  width: 100%;
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

const StyledFilterControlContainer = styled.div`
  width: 100%;
`;

const FilterControl: React.FC<FilterProps> = ({
  filter,
  icon,
  onFilterSelectionChange,
  directPathToChild,
}) => {
  const { name = '<undefined>' } = filter;
  return (
    <StyledFilterControlContainer>
      <StyledFilterControlTitleBox>
        <StyledFilterControlTitle data-test="filter-control-name">
          {name}
        </StyledFilterControlTitle>
        <div data-test="filter-icon">{icon}</div>
      </StyledFilterControlTitleBox>
      <FilterValue
        filter={filter}
        directPathToChild={directPathToChild}
        onFilterSelectionChange={onFilterSelectionChange}
      />
    </StyledFilterControlContainer>
  );
};

export default FilterControl;
