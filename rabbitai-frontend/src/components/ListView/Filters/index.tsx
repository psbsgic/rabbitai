
import React from 'react';
import { styled, withTheme } from '@rabbitai-ui/core';

import {
  FilterValue,
  Filters,
  InternalFilter,
} from 'src/components/ListView/types';
import SearchFilter from './Search';
import SelectFilter from './Select';
import DateRangeFilter from './DateRange';

interface UIFiltersProps {
  filters: Filters;
  internalFilters: InternalFilter[];
  updateFilterValue: (id: number, value: FilterValue['value']) => void;
}

const FilterWrapper = styled.div`
  display: inline-block;
`;

function UIFilters({
  filters,
  internalFilters = [],
  updateFilterValue,
}: UIFiltersProps) {
  return (
    <FilterWrapper>
      {filters.map(
        (
          {
            Header,
            fetchSelects,
            id,
            input,
            paginate,
            selects,
            unfilteredLabel,
          },
          index,
        ) => {
          const initialValue =
            internalFilters[index] && internalFilters[index].value;
          if (input === 'select') {
            return (
              <SelectFilter
                Header={Header}
                emptyLabel={unfilteredLabel}
                fetchSelects={fetchSelects}
                initialValue={initialValue}
                key={id}
                name={id}
                onSelect={(value: any) => updateFilterValue(index, value)}
                paginate={paginate}
                selects={selects}
              />
            );
          }
          if (input === 'search' && typeof Header === 'string') {
            return (
              <SearchFilter
                Header={Header}
                initialValue={initialValue}
                key={id}
                name={id}
                onSubmit={(value: string) => updateFilterValue(index, value)}
              />
            );
          }
          if (input === 'datetime_range') {
            return (
              <DateRangeFilter
                Header={Header}
                initialValue={initialValue}
                key={id}
                name={id}
                onSubmit={value => updateFilterValue(index, value)}
              />
            );
          }
          return null;
        },
      )}
    </FilterWrapper>
  );
}

export default withTheme(UIFilters);
