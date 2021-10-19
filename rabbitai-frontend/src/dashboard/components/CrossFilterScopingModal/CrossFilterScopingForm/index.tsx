import React, { FC } from 'react';
import { FormInstance } from 'antd/lib/form';
import FilterScope from 'src/dashboard/components/nativeFilters/FiltersConfigModal/FiltersConfigForm/FilterScope/FilterScope';
import { setCrossFilterFieldValues } from 'src/dashboard/components/CrossFilterScopingModal/utils';
import { Scope } from 'src/dashboard/components/nativeFilters/types';
import { useForceUpdate } from 'src/dashboard/components/nativeFilters/FiltersConfigModal/FiltersConfigForm/utils';
import { CrossFilterScopingFormType } from 'src/dashboard/components/CrossFilterScopingModal/types';

type CrossFilterScopingFormProps = {
  chartId: number;
  scope: Scope;
  form: FormInstance<CrossFilterScopingFormType>;
};

const CrossFilterScopingForm: FC<CrossFilterScopingFormProps> = ({
  form,
  scope,
  chartId,
}) => {
  const forceUpdate = useForceUpdate();
  const formScope = form.getFieldValue('scope');
  const formScoping = form.getFieldValue('scoping');
  return (
    <FilterScope
      updateFormValues={(values: any) => {
        setCrossFilterFieldValues(form, {
          ...values,
        });
      }}
      filterScope={scope}
      chartId={chartId}
      formFilterScope={formScope}
      forceUpdate={forceUpdate}
      formScopingType={formScoping}
    />
  );
};

export default CrossFilterScopingForm;
