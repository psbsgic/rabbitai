/* eslint-disable no-param-reassign */
import {
  AppSection,
  DataMask,
  ensureIsArray,
  ExtraFormData,
  GenericDataType,
  JsonObject,
  smartDateDetailedFormatter,
  t,
  tn,
} from '@superset-ui/core';
import React, { useCallback, useEffect, useState, useMemo } from 'react';
import { Select } from 'src/components';
import debounce from 'lodash/debounce';
import { SLOW_DEBOUNCE } from 'src/constants';
import { useImmerReducer } from 'use-immer';
import { FormItemProps } from 'antd/lib/form';
import { PluginFilterSelectProps, SelectValue } from './types';
import { StyledFormItem, FilterPluginStyle, StatusMessage } from '../common';
import { getDataRecordFormatter, getSelectExtraFormData } from '../../utils';

type DataMaskAction =
  | { type: 'ownState'; ownState: JsonObject }
  | {
      type: 'filterState';
      __cache: JsonObject;
      extraFormData: ExtraFormData;
      filterState: { value: SelectValue; label?: string };
    };

function reducer(
  draft: DataMask & { __cache?: JsonObject },
  action: DataMaskAction,
) {
  switch (action.type) {
    case 'ownState':
      draft.ownState = {
        ...draft.ownState,
        ...action.ownState,
      };
      return draft;
    case 'filterState':
      draft.extraFormData = action.extraFormData;
      // eslint-disable-next-line no-underscore-dangle
      draft.__cache = action.__cache;
      draft.filterState = { ...draft.filterState, ...action.filterState };
      return draft;
    default:
      return draft;
  }
}

export default function PluginFilterSelect(props: PluginFilterSelectProps) {
  const {
    coltypeMap,
    data,
    filterState,
    formData,
    height,
    isRefreshing,
    width,
    setDataMask,
    setFocusedFilter,
    unsetFocusedFilter,
    appSection,
  } = props;
  const {
    enableEmptyFilter,
    multiSelect,
    showSearch,
    inverseSelection,
    inputRef,
    defaultToFirstItem,
    searchAllOptions,
  } = formData;
  const groupby = ensureIsArray<string>(formData.groupby);
  const [col] = groupby;
  const [initialColtypeMap] = useState(coltypeMap);
  const [dataMask, dispatchDataMask] = useImmerReducer(reducer, {
    extraFormData: {},
    filterState,
  });
  const updateDataMask = useCallback(
    (values: SelectValue) => {
      const emptyFilter =
        enableEmptyFilter && !inverseSelection && !values?.length;

      const suffix =
        inverseSelection && values?.length ? ` (${t('excluded')})` : '';

      dispatchDataMask({
        type: 'filterState',
        __cache: filterState,
        extraFormData: getSelectExtraFormData(
          col,
          values,
          emptyFilter,
          inverseSelection,
        ),
        filterState: {
          ...filterState,
          label: values?.length
            ? `${(values || []).join(', ')}${suffix}`
            : undefined,
          value:
            appSection === AppSection.FILTER_CONFIG_MODAL && defaultToFirstItem
              ? undefined
              : values,
        },
      });
    },
    [
      appSection,
      col,
      defaultToFirstItem,
      dispatchDataMask,
      enableEmptyFilter,
      inverseSelection,
      JSON.stringify(filterState),
    ],
  );

  useEffect(() => {
    updateDataMask(filterState.value);
  }, [JSON.stringify(filterState.value)]);

  const isDisabled =
    appSection === AppSection.FILTER_CONFIG_MODAL && defaultToFirstItem;

  const debouncedOwnStateFunc = useCallback(
    debounce((val: string) => {
      dispatchDataMask({
        type: 'ownState',
        ownState: {
          coltypeMap: initialColtypeMap,
          search: val,
        },
      });
    }, SLOW_DEBOUNCE),
    [],
  );

  const searchWrapper = (val: string) => {
    if (searchAllOptions) {
      debouncedOwnStateFunc(val);
    }
  };

  const clearSuggestionSearch = () => {
    if (searchAllOptions) {
      dispatchDataMask({
        type: 'ownState',
        ownState: {
          coltypeMap: initialColtypeMap,
          search: null,
        },
      });
    }
  };

  const handleBlur = () => {
    clearSuggestionSearch();
    unsetFocusedFilter();
  };

  const datatype: GenericDataType = coltypeMap[col];
  const labelFormatter = useMemo(
    () =>
      getDataRecordFormatter({
        timeFormatter: smartDateDetailedFormatter,
      }),
    [],
  );

  const handleChange = (value?: SelectValue | number | string) => {
    const values = ensureIsArray(value);
    if (values.length === 0) {
      updateDataMask(null);
    } else {
      updateDataMask(values);
    }
  };

  useEffect(() => {
    if (defaultToFirstItem && filterState.value === undefined) {
      // initialize to first value if set to default to first item
      const firstItem: SelectValue = data[0]
        ? (groupby.map(col => data[0][col]) as string[])
        : null;
      // firstItem[0] !== undefined for a case when groupby changed but new data still not fetched
      // TODO: still need repopulate default value in config modal when column changed
      if (firstItem && firstItem[0] !== undefined) {
        updateDataMask(firstItem);
      }
    } else if (isDisabled) {
      // empty selection if filter is disabled
      updateDataMask(null);
    } else {
      // reset data mask based on filter state
      updateDataMask(filterState.value);
    }
  }, [
    col,
    isDisabled,
    defaultToFirstItem,
    enableEmptyFilter,
    inverseSelection,
    updateDataMask,
    data,
    groupby,
    JSON.stringify(filterState),
  ]);

  useEffect(() => {
    setDataMask(dataMask);
  }, [JSON.stringify(dataMask)]);

  const placeholderText =
    data.length === 0
      ? t('No data')
      : tn('%s option', '%s options', data.length, data.length);

  const formItemData: FormItemProps = {};
  if (filterState.validateMessage) {
    formItemData.extra = (
      <StatusMessage status={filterState.validateStatus}>
        {filterState.validateMessage}
      </StatusMessage>
    );
  }

  const options = useMemo(() => {
    const options: { label: string; value: string | number }[] = [];
    data.forEach(row => {
      const [value] = groupby.map(col => row[col]);
      options.push({
        label: labelFormatter(value, datatype),
        value: typeof value === 'number' ? value : String(value),
      });
    });
    return options;
  }, [data, datatype, groupby, labelFormatter]);

  return (
    <FilterPluginStyle height={height} width={width}>
      <StyledFormItem
        validateStatus={filterState.validateStatus}
        {...formItemData}
      >
        <Select
          allowClear
          allowNewOptions
          // @ts-ignore
          value={filterState.value || []}
          disabled={isDisabled}
          showSearch={showSearch}
          mode={multiSelect ? 'multiple' : 'single'}
          placeholder={placeholderText}
          onSearch={searchWrapper}
          onSelect={clearSuggestionSearch}
          onBlur={handleBlur}
          onMouseEnter={setFocusedFilter}
          onMouseLeave={unsetFocusedFilter}
          // @ts-ignore
          onChange={handleChange}
          ref={inputRef}
          loading={isRefreshing}
          maxTagCount={5}
          invertSelection={inverseSelection}
          options={options}
        />
      </StyledFormItem>
    </FilterPluginStyle>
  );
}
