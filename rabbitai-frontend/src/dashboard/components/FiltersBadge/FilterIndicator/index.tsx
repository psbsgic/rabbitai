

import { SearchOutlined } from '@ant-design/icons';
import React, { FC } from 'react';
import { getFilterValueForDisplay } from 'src/dashboard/components/nativeFilters/FilterBar/FilterSets/utils';
import {
  FilterValue,
  Item,
  ItemIcon,
  Title,
} from 'src/dashboard/components/FiltersBadge/Styles';
import { Indicator } from 'src/dashboard/components/FiltersBadge/selectors';

export interface IndicatorProps {
  indicator: Indicator;
  onClick?: (path: string[]) => void;
}

const FilterIndicator: FC<IndicatorProps> = ({
  indicator: { column, name, value, path = [] },
  onClick = () => {},
}) => {
  const resultValue = getFilterValueForDisplay(value);
  return (
    <Item onClick={() => onClick([...path, `LABEL-${column}`])}>
      <Title bold>
        <ItemIcon>
          <SearchOutlined />
        </ItemIcon>
        {name}
        {resultValue ? ': ' : ''}
      </Title>
      <FilterValue>{resultValue}</FilterValue>
    </Item>
  );
};

export default FilterIndicator;
