import {
  getNumberFormatter,
  NumberFormats,
  styled,
  t,
} from '@superset-ui/core';
import React, { useEffect, useState } from 'react';
import { Slider } from 'src/common/components';
import { rgba } from 'emotion-rgba';
import { FormItemProps } from 'antd/lib/form';
import { PluginFilterRangeProps } from './types';
import { StatusMessage, StyledFormItem, FilterPluginStyle } from '../common';
import { getRangeExtraFormData } from '../../utils';

const Wrapper = styled.div<{ validateStatus?: 'error' | 'warning' | 'info' }>`
  ${({ theme, validateStatus }) => `
    border: 1px solid transparent;
    &:focus {
      border: 1px solid
        ${theme.colors[validateStatus || 'primary']?.base};
      outline: 0;
      box-shadow: 0 0 0 3px
        ${rgba(theme.colors[validateStatus || 'primary']?.base, 0.2)};
    }
    & .ant-slider {
      margin-top: ${theme.gridUnit}px;
      margin-bottom: ${theme.gridUnit * 5}px;

      & .ant-slider-track {
        background-color: ${
          validateStatus && theme.colors[validateStatus]?.light1
        };
      }
      & .ant-slider-handle {
        border: ${
          validateStatus && `2px solid ${theme.colors[validateStatus]?.light1}`
        };
        &:focus {
          box-shadow: 0 0 0 3px
            ${rgba(theme.colors[validateStatus || 'primary']?.base, 0.2)};
        }
      }
      &:hover {
        & .ant-slider-track {
          background-color: ${
            validateStatus && theme.colors[validateStatus]?.base
          };
        }
        & .ant-slider-handle {
          border: ${
            validateStatus && `2px solid ${theme.colors[validateStatus]?.base}`
          };
        }
      }
    }
  `}
`;

export default function RangeFilterPlugin(props: PluginFilterRangeProps) {
  const {
    data,
    formData,
    height,
    width,
    setDataMask,
    setFocusedFilter,
    unsetFocusedFilter,
    filterState,
  } = props;
  const numberFormatter = getNumberFormatter(NumberFormats.SMART_NUMBER);

  const [row] = data;
  // @ts-ignore
  const { min, max }: { min: number; max: number } = row;
  const { groupby, defaultValue, inputRef } = formData;
  const [col = ''] = groupby || [];
  const [value, setValue] = useState<[number, number]>(
    defaultValue ?? [min, max],
  );
  const [marks, setMarks] = useState<{ [key: number]: string }>({});

  const getBounds = (
    value: [number, number],
  ): { lower: number | null; upper: number | null } => {
    const [lowerRaw, upperRaw] = value;
    return {
      lower: lowerRaw > min ? lowerRaw : null,
      upper: upperRaw < max ? upperRaw : null,
    };
  };

  const getLabel = (lower: number | null, upper: number | null): string => {
    if (lower !== null && upper !== null) {
      return `${numberFormatter(lower)} ≤ x ≤ ${numberFormatter(upper)}`;
    }
    if (lower !== null) {
      return `x ≥ ${numberFormatter(lower)}`;
    }
    if (upper !== null) {
      return `x ≤ ${numberFormatter(upper)}`;
    }
    return '';
  };

  const getMarks = (
    lower: number | null,
    upper: number | null,
  ): { [key: number]: string } => {
    const newMarks: { [key: number]: string } = {};
    if (lower !== null) {
      newMarks[lower] = numberFormatter(lower);
    }
    if (upper !== null) {
      newMarks[upper] = numberFormatter(upper);
    }
    return newMarks;
  };

  const handleAfterChange = (value: [number, number]): void => {
    setValue(value);
    const { lower, upper } = getBounds(value);
    setMarks(getMarks(lower, upper));

    setDataMask({
      extraFormData: getRangeExtraFormData(col, lower, upper),
      filterState: {
        value: lower !== null || upper !== null ? value : null,
        label: getLabel(lower, upper),
      },
    });
  };

  const handleChange = (value: [number, number]) => {
    setValue(value);
  };

  useEffect(() => {
    // when switch filter type and queriesData still not updated we need ignore this case (in FilterBar)
    if (row?.min === undefined && row?.max === undefined) {
      return;
    }
    handleAfterChange(filterState.value ?? [min, max]);
  }, [JSON.stringify(filterState.value), JSON.stringify(data)]);

  const formItemData: FormItemProps = {};
  if (filterState.validateMessage) {
    formItemData.extra = (
      <StatusMessage status={filterState.validateStatus}>
        {filterState.validateMessage}
      </StatusMessage>
    );
  }
  return (
    <FilterPluginStyle height={height} width={width}>
      {Number.isNaN(Number(min)) || Number.isNaN(Number(max)) ? (
        <h4>{t('Chosen non-numeric column')}</h4>
      ) : (
        <StyledFormItem {...formItemData}>
          <Wrapper
            tabIndex={-1}
            ref={inputRef}
            validateStatus={filterState.validateStatus}
            onFocus={setFocusedFilter}
            onBlur={unsetFocusedFilter}
            onMouseEnter={setFocusedFilter}
            onMouseLeave={unsetFocusedFilter}
          >
            <Slider
              range
              min={min}
              max={max}
              value={value ?? [min, max]}
              onAfterChange={handleAfterChange}
              onChange={handleChange}
              tipFormatter={value => numberFormatter(value)}
              marks={marks}
            />
          </Wrapper>
        </StyledFormItem>
      )}
    </FilterPluginStyle>
  );
}
