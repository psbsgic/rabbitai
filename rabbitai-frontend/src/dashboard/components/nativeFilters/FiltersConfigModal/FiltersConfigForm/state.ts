
import { useEffect } from 'react';
import { FormInstance } from 'antd/lib/form';
import { NativeFiltersForm } from '../types';
import { setNativeFilterFieldValues, useForceUpdate } from './utils';

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
