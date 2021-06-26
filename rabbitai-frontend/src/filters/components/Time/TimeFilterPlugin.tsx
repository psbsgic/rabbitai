
import { styled } from '@rabbitai-ui/core';
import React, { useState, useEffect } from 'react';
import DateFilterControl from 'src/explore/components/controls/DateFilterControl';
import { PluginFilterTimeProps } from './types';
import { Styles } from '../common';

const DEFAULT_VALUE = 'Last week';

const TimeFilterStyles = styled(Styles)`
  overflow-x: scroll;
`;

const ControlContainer = styled.div`
  display: inline-block;
`;

export default function TimeFilterPlugin(props: PluginFilterTimeProps) {
  const {
    formData,
    setDataMask,
    setFocusedFilter,
    unsetFocusedFilter,
    width,
    filterState,
  } = props;
  const { defaultValue } = formData;

  const [value, setValue] = useState<string>(defaultValue ?? DEFAULT_VALUE);

  const handleTimeRangeChange = (timeRange: string): void => {
    setValue(timeRange);

    setDataMask({
      extraFormData: {
        time_range: timeRange,
      },
      filterState: { value: timeRange },
    });
  };

  useEffect(() => {
    handleTimeRangeChange(filterState.value ?? DEFAULT_VALUE);
  }, [filterState.value]);

  useEffect(() => {
    handleTimeRangeChange(defaultValue ?? DEFAULT_VALUE);
  }, [defaultValue]);

  return (
    // @ts-ignore
    <TimeFilterStyles width={width}>
      <ControlContainer
        onMouseEnter={setFocusedFilter}
        onMouseLeave={unsetFocusedFilter}
      >
        <DateFilterControl
          value={value}
          name="time_range"
          onChange={handleTimeRangeChange}
        />
      </ControlContainer>
    </TimeFilterStyles>
  );
}
