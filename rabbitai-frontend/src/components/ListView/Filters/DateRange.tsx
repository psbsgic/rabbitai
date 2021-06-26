
import React, { useState, useMemo } from 'react';
import moment, { Moment } from 'moment';
import { styled } from '@rabbitai-ui/core';
import { RangePicker as AntRangePicker } from 'src/components/DatePicker';
import { FilterContainer, BaseFilter, FilterTitle } from './Base';

interface DateRangeFilterProps extends BaseFilter {
  onSubmit: (val: number[]) => void;
  name: string;
}

type ValueState = [number, number];

const RangePicker = styled(AntRangePicker)`
  padding: 0 11px;
  transform: translateX(-7px);
`;

const RangeFilterContainer = styled(FilterContainer)`
  margin-right: 1em;
`;

export default function DateRangeFilter({
  Header,
  initialValue,
  onSubmit,
}: DateRangeFilterProps) {
  const [value, setValue] = useState<ValueState | null>(initialValue ?? null);
  const momentValue = useMemo((): [Moment, Moment] | null => {
    if (!value || (Array.isArray(value) && !value.length)) return null;
    return [moment(value[0]), moment(value[1])];
  }, [value]);

  return (
    <RangeFilterContainer>
      <FilterTitle>{Header}:</FilterTitle>
      <RangePicker
        showTime
        bordered={false}
        value={momentValue}
        onChange={momentRange => {
          if (!momentRange) {
            setValue(null);
            onSubmit([]);
            return;
          }
          const changeValue = [
            momentRange[0]?.valueOf() ?? 0,
            momentRange[1]?.valueOf() ?? 0,
          ] as ValueState;
          setValue(changeValue);
          onSubmit(changeValue);
        }}
      />
    </RangeFilterContainer>
  );
}
