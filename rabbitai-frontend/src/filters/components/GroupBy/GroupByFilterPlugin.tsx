import { ensureIsArray, ExtraFormData, t, tn } from '@rabbitai-ui/core';
import React, { useEffect, useState } from 'react';
import { Select } from 'src/common/components';
import { Styles, StyledSelect } from '../common';
import { PluginFilterGroupByProps } from './types';

const { Option } = Select;

export default function PluginFilterGroupBy(props: PluginFilterGroupByProps) {
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
  const { defaultValue, inputRef, multiSelect } = formData;

  const [value, setValue] = useState<string[]>(defaultValue ?? []);

  const handleChange = (value?: string[] | string | null) => {
    const resultValue: string[] = ensureIsArray<string>(value);
    setValue(resultValue);
    const extraFormData: ExtraFormData = {};
    if (resultValue.length) {
      extraFormData.interactive_groupby = resultValue;
    }

    setDataMask({
      filterState: { value: resultValue.length ? resultValue : null },
      extraFormData,
    });
  };

  useEffect(() => {
    handleChange(filterState.value);
  }, [JSON.stringify(filterState.value), multiSelect]);

  useEffect(() => {
    handleChange(defaultValue ?? null);
    // I think after Config Modal update some filter it re-creates default value for all other filters
    // so we can process it like this `JSON.stringify` or start to use `Immer`
  }, [JSON.stringify(defaultValue), multiSelect]);

  const columns = data || [];
  const placeholderText =
    columns.length === 0
      ? t('No columns')
      : tn('%s option', '%s options', columns.length, columns.length);
  return (
    <Styles height={height} width={width}>
      <StyledSelect
        allowClear
        value={value}
        placeholder={placeholderText}
        mode={multiSelect ? 'multiple' : undefined}
        // @ts-ignore
        onChange={handleChange}
        onBlur={unsetFocusedFilter}
        onFocus={setFocusedFilter}
        ref={inputRef}
      >
        {columns.map(
          (row: { column_name: string; verbose_name: string | null }) => {
            const { column_name: columnName, verbose_name: verboseName } = row;
            return (
              <Option key={columnName} value={columnName}>
                {verboseName ?? columnName}
              </Option>
            );
          },
        )}
      </StyledSelect>
    </Styles>
  );
}
