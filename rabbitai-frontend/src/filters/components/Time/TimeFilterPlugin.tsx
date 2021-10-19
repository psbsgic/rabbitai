import { styled } from '@superset-ui/core';
import React, { useEffect } from 'react';
import DateFilterControl from 'src/explore/components/controls/DateFilterControl';
import { NO_TIME_RANGE } from 'src/explore/constants';
import { PluginFilterTimeProps } from './types';
import { FilterPluginStyle } from '../common';

const TimeFilterStyles = styled(FilterPluginStyle)`
  overflow-x: auto;
`;

const ControlContainer = styled.div<{
  validateStatus?: 'error' | 'warning' | 'info';
}>`
  padding: 2px;
  & > span,
  & > span:hover {
    border: 2px solid transparent;
    display: inline-block;
    border: ${({ theme, validateStatus }) =>
      validateStatus && `2px solid ${theme.colors[validateStatus]?.base}`};
  }
  &:focus {
    & > span {
      border: 2px solid
        ${({ theme, validateStatus }) =>
          validateStatus
            ? theme.colors[validateStatus]?.base
            : theme.colors.primary.base};
      outline: 0;
      box-shadow: 0 0 0 2px
        ${({ validateStatus }) =>
          validateStatus
            ? 'rgba(224, 67, 85, 12%)'
            : 'rgba(32, 167, 201, 0.2)'};
    }
  }
`;

export default function TimeFilterPlugin(props: PluginFilterTimeProps) {
  const {
    setDataMask,
    setFocusedFilter,
    unsetFocusedFilter,
    width,
    height,
    filterState,
    formData: { inputRef },
  } = props;

  const handleTimeRangeChange = (timeRange?: string): void => {
    const isSet = timeRange && timeRange !== NO_TIME_RANGE;
    setDataMask({
      extraFormData: isSet
        ? {
            time_range: timeRange,
          }
        : {},
      filterState: {
        value: isSet ? timeRange : undefined,
      },
    });
  };

  useEffect(() => {
    handleTimeRangeChange(filterState.value);
  }, [filterState.value]);

  return props.formData?.inView ? (
    // @ts-ignore
    <TimeFilterStyles width={width} height={height}>
      <ControlContainer
        tabIndex={-1}
        ref={inputRef}
        validateStatus={filterState.validateStatus}
        onFocus={setFocusedFilter}
        onBlur={unsetFocusedFilter}
        onMouseEnter={setFocusedFilter}
        onMouseLeave={unsetFocusedFilter}
      >
        <DateFilterControl
          value={filterState.value || NO_TIME_RANGE}
          name="time_range"
          onChange={handleTimeRangeChange}
          type={filterState.validateStatus}
        />
      </ControlContainer>
    </TimeFilterStyles>
  ) : null;
}
