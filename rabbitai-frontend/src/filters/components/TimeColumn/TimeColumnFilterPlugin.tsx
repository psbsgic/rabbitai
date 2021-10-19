import {
  ensureIsArray,
  ExtraFormData,
  GenericDataType,
  t,
  tn,
} from '@superset-ui/core';
import React, { useEffect, useState } from 'react';
import { Select } from 'src/components';
import { FormItemProps } from 'antd/lib/form';
import { FilterPluginStyle, StyledFormItem, StatusMessage } from '../common';
import { PluginFilterTimeColumnProps } from './types';

export default function PluginFilterTimeColumn(
  props: PluginFilterTimeColumnProps,
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

  const handleChange = (value?: string[] | string | null) => {
    const resultValue: string[] = ensureIsArray<string>(value);
    setValue(resultValue);
    const extraFormData: ExtraFormData = {};
    if (resultValue.length) {
      extraFormData.granularity_sqla = resultValue[0];
    }

    setDataMask({
      extraFormData,
      filterState: {
        value: resultValue.length ? resultValue : null,
      },
    });
  };

  useEffect(() => {
    handleChange(defaultValue ?? null);
    // I think after Config Modal update some filter it re-creates default value for all other filters
    // so we can process it like this `JSON.stringify` or start to use `Immer`
  }, [JSON.stringify(defaultValue)]);

  useEffect(() => {
    handleChange(filterState.value ?? null);
  }, [JSON.stringify(filterState.value)]);

  const timeColumns = (data || []).filter(
    row => row.dtype === GenericDataType.TEMPORAL,
  );

  const placeholderText =
    timeColumns.length === 0
      ? t('No time columns')
      : tn('%s option', '%s options', timeColumns.length, timeColumns.length);

  const formItemData: FormItemProps = {};
  if (filterState.validateMessage) {
    formItemData.extra = (
      <StatusMessage status={filterState.validateStatus}>
        {filterState.validateMessage}
      </StatusMessage>
    );
  }

  const options = timeColumns.map(
    (row: { column_name: string; verbose_name: string | null }) => {
      const { column_name: columnName, verbose_name: verboseName } = row;
      return {
        label: verboseName ?? columnName,
        value: columnName,
      };
    },
  );

  return (
    <FilterPluginStyle height={height} width={width}>
      <StyledFormItem
        validateStatus={filterState.validateStatus}
        {...formItemData}
      >
        <Select
          allowClear
          value={value}
          placeholder={placeholderText}
          // @ts-ignore
          onChange={handleChange}
          onMouseEnter={setFocusedFilter}
          onMouseLeave={unsetFocusedFilter}
          ref={inputRef}
          options={options}
        />
      </StyledFormItem>
    </FilterPluginStyle>
  );
}
