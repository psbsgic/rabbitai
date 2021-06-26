
import React, { FC, useEffect, useState } from 'react';
import {
  Behavior,
  SetDataMaskHook,
  SuperChart,
  AppSection,
} from '@rabbitai-ui/core';
import { FormInstance } from 'antd/lib/form';
import Loading from 'src/components/Loading';
import { NativeFiltersForm } from '../types';
import { getFormData } from '../../utils';

type DefaultValueProps = {
  filterId: string;
  setDataMask: SetDataMaskHook;
  hasDataset: boolean;
  form: FormInstance<NativeFiltersForm>;
  formData: ReturnType<typeof getFormData>;
  enableNoResults: boolean;
};

const DefaultValue: FC<DefaultValueProps> = ({
  filterId,
  hasDataset,
  form,
  setDataMask,
  formData,
  enableNoResults,
}) => {
  const [loading, setLoading] = useState(hasDataset);
  const formFilter = (form.getFieldValue('filters') || {})[filterId];
  const queriesData = formFilter?.defaultValueQueriesData;

  useEffect(() => {
    if (!hasDataset || queriesData !== null) {
      setLoading(false);
    } else {
      setLoading(true);
    }
  }, [hasDataset, queriesData]);

  return loading ? (
    <Loading position="inline-centered" />
  ) : (
    <SuperChart
      height={25}
      width={250}
      appSection={AppSection.FILTER_CONFIG_MODAL}
      behaviors={[Behavior.NATIVE_FILTER]}
      formData={formData}
      // For charts that don't have datasource we need workaround for empty placeholder
      queriesData={
        hasDataset ? formFilter?.defaultValueQueriesData : [{ data: [{}] }]
      }
      chartType={formFilter?.filterType}
      hooks={{ setDataMask }}
      enableNoResults={enableNoResults}
      filterState={formFilter.defaultDataMask?.filterState}
    />
  );
};

export default DefaultValue;
