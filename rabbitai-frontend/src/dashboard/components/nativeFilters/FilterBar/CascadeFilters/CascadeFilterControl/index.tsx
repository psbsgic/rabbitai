import React from 'react';
import { styled, DataMask } from '@superset-ui/core';
import FilterControl from 'src/dashboard/components/nativeFilters/FilterBar/FilterControls/FilterControl';
import { CascadeFilter } from 'src/dashboard/components/nativeFilters/FilterBar/CascadeFilters/types';
import { Filter } from 'src/dashboard/components/nativeFilters/types';
import { DataMaskStateWithId } from 'src/dataMask/types';

export interface CascadeFilterControlProps {
  dataMaskSelected?: DataMaskStateWithId;
  filter: CascadeFilter;
  directPathToChild?: string[];
  onFilterSelectionChange: (filter: Filter, dataMask: DataMask) => void;
}

const StyledDiv = styled.div`
  display: flex;
  width: 100%;
  flex-direction: column;
  align-items: center;

  .ant-form-item {
    margin-bottom: ${({ theme }) => theme.gridUnit * 4}px;
  }
`;

const CascadeFilterControl: React.FC<CascadeFilterControlProps> = ({
  dataMaskSelected,
  filter,
  directPathToChild,
  onFilterSelectionChange,
}) => (
  <>
    <FilterControl
      dataMaskSelected={dataMaskSelected}
      filter={filter}
      directPathToChild={directPathToChild}
      onFilterSelectionChange={onFilterSelectionChange}
    />
    <StyledDiv>
      {filter.cascadeChildren?.map(childFilter => (
        <CascadeFilterControl
          key={childFilter.id}
          dataMaskSelected={dataMaskSelected}
          filter={childFilter}
          directPathToChild={directPathToChild}
          onFilterSelectionChange={onFilterSelectionChange}
        />
      ))}
    </StyledDiv>
  </>
);

export default CascadeFilterControl;
