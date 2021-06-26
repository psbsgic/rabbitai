
import React from 'react';
import { styled, DataMask } from '@rabbitai-ui/core';
import Icon from 'src/components/Icon';
import FilterControl from 'src/dashboard/components/nativeFilters/FilterBar/FilterControls/FilterControl';
import { CascadeFilter } from 'src/dashboard/components/nativeFilters/FilterBar/CascadeFilters/types';
import { Filter } from 'src/dashboard/components/nativeFilters/types';

export interface CascadeFilterControlProps {
  filter: CascadeFilter;
  directPathToChild?: string[];
  onFilterSelectionChange: (filter: Filter, dataMask: DataMask) => void;
}

const StyledCascadeChildrenList = styled.ul`
  list-style-type: none;
  & > * {
    list-style-type: none;
  }
`;

const StyledFilterControlBox = styled.div`
  display: flex;
`;

const StyledCaretIcon = styled(Icon)`
  margin-top: ${({ theme }) => -theme.gridUnit}px;
`;

const CascadeFilterControl: React.FC<CascadeFilterControlProps> = ({
  filter,
  directPathToChild,
  onFilterSelectionChange,
}) => (
  <>
    <StyledFilterControlBox>
      <StyledCaretIcon name="caret-down" />
      <FilterControl
        filter={filter}
        directPathToChild={directPathToChild}
        onFilterSelectionChange={onFilterSelectionChange}
      />
    </StyledFilterControlBox>

    <StyledCascadeChildrenList>
      {filter.cascadeChildren?.map(childFilter => (
        <li key={childFilter.id}>
          <CascadeFilterControl
            filter={childFilter}
            directPathToChild={directPathToChild}
            onFilterSelectionChange={onFilterSelectionChange}
          />
        </li>
      ))}
    </StyledCascadeChildrenList>
  </>
);

export default CascadeFilterControl;
