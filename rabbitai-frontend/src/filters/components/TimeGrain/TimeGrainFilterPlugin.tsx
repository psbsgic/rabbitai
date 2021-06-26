
import {
  ensureIsArray,
  ExtraFormData,
  t,
  TimeGranularity,
  tn,
} from '@rabbitai-ui/core';
import React, { useEffect, useState } from 'react';
import { Select } from 'src/common/components';
import { Styles, StyledSelect } from '../common';
import { PluginFilterTimeGrainProps } from './types';

const { Option } = Select;

export default function PluginFilterTimegrain(
  props: PluginFilterTimeGrainProps,
) {
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
  const { defaultValue, inputRef } = formData;

  const [value, setValue] = useState<string[]>(defaultValue ?? []);

  const handleChange = (values: string[] | string | undefined | null) => {
    const resultValue: string[] = ensureIsArray<string>(values);
    const [timeGrain] = resultValue;

    const extraFormData: ExtraFormData = {};
    if (timeGrain) {
      extraFormData.time_grain_sqla = timeGrain as TimeGranularity;
    }
    setValue(resultValue);
    setDataMask({
      extraFormData,
      filterState: {
        value: resultValue.length ? resultValue : null,
      },
    });
  };

  useEffect(() => {
    handleChange(filterState.value ?? []);
  }, [JSON.stringify(filterState.value)]);

  useEffect(() => {
    handleChange(defaultValue ?? []);
    // I think after Config Modal update some filter it re-creates default value for all other filters
    // so we can process it like this `JSON.stringify` or start to use `Immer`
  }, [JSON.stringify(defaultValue)]);

  const placeholderText =
    (data || []).length === 0
      ? t('No data')
      : tn('%s option', '%s options', data.length, data.length);
  return (
    <Styles height={height} width={width}>
      <StyledSelect
        allowClear
        value={value}
        placeholder={placeholderText}
        // @ts-ignore
        onChange={handleChange}
        onBlur={unsetFocusedFilter}
        onFocus={setFocusedFilter}
        ref={inputRef}
      >
        {(data || []).map((row: { name: string; duration: string }) => {
          const { name, duration } = row;
          return (
            <Option key={duration} value={duration}>
              {name}
            </Option>
          );
        })}
      </StyledSelect>
    </Styles>
  );
}
