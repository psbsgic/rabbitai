import { useEffect, useState } from 'react';
import { FormInstance } from 'antd/lib/form';
import { t } from '@superset-ui/core';
import { NativeFiltersForm, NativeFiltersFormItem } from '../types';
import { setNativeFilterFieldValues, useForceUpdate } from './utils';
import { Filter } from '../../types';

// When some fields in form changed we need re-fetch data for Filter defaultValue
// eslint-disable-next-line import/prefer-default-export
export const useBackendFormUpdate = (
  form: FormInstance<NativeFiltersForm>,
  filterId: string,
) => {
  const forceUpdate = useForceUpdate();
  const formFilter = (form.getFieldValue('filters') || {})[filterId];
  useEffect(() => {
    setNativeFilterFieldValues(form, filterId, {
      isDataDirty: true,
      defaultValueQueriesData: null,
    });
    forceUpdate();
  }, [
    form,
    formFilter?.filterType,
    formFilter?.column,
    formFilter?.dataset?.value,
    JSON.stringify(formFilter?.adhoc_filters),
    formFilter?.time_range,
    forceUpdate,
    filterId,
  ]);
};

export const useDefaultValue = (
  formFilter?: NativeFiltersFormItem,
  filterToEdit?: Filter,
): [boolean, boolean, string, Function] => {
  const enableEmptyFilter = !!formFilter?.controlValues?.enableEmptyFilter;
  const defaultToFirstItem = !!formFilter?.controlValues?.defaultToFirstItem;

  const [hasDefaultValue, setHasPartialDefaultValue] = useState(false);
  const [isRequired, setIsRequired] = useState(enableEmptyFilter);
  const [defaultValueTooltip, setDefaultValueTooltip] = useState('');

  const setHasDefaultValue = (value = false) => {
    const required = enableEmptyFilter && !defaultToFirstItem;
    setIsRequired(required);
    setHasPartialDefaultValue(required ? true : value);
  };

  useEffect(() => {
    setHasDefaultValue(
      defaultToFirstItem
        ? false
        : !!formFilter?.defaultDataMask?.filterState?.value,
    );
    // TODO: this logic should be unhardcoded
  }, [defaultToFirstItem, enableEmptyFilter]);

  useEffect(() => {
    setHasDefaultValue(
      defaultToFirstItem
        ? false
        : !!filterToEdit?.defaultDataMask?.filterState?.value,
    );
  }, []);

  useEffect(() => {
    let tooltip = '';
    if (defaultToFirstItem) {
      tooltip = t(
        'Default value set automatically when "Default to first item" is checked',
      );
    } else if (isRequired) {
      tooltip = t('Default value must be set when "Required" is checked');
    } else if (hasDefaultValue) {
      tooltip = t(
        'Default value must be set when "Filter has default value" is checked',
      );
    }
    setDefaultValueTooltip(tooltip);
  }, [hasDefaultValue, isRequired, defaultToFirstItem]);

  return [hasDefaultValue, isRequired, defaultValueTooltip, setHasDefaultValue];
};
