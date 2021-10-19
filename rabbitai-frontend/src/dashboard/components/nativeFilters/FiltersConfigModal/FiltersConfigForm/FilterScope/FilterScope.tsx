import React, { FC, useCallback, useState } from 'react';
import { t, styled } from '@superset-ui/core';
import { Radio } from 'src/components/Radio';
import { Form, Typography } from 'src/common/components';
import { useComponentDidUpdate } from 'src/common/hooks/useComponentDidUpdate/useComponentDidUpdate';
import { Scope } from '../../../types';
import { ScopingType } from './types';
import ScopingTree from './ScopingTree';
import { getDefaultScopeValue, isScopingAll } from './utils';

type FilterScopeProps = {
  pathToFormValue?: string[];
  updateFormValues: (values: any) => void;
  formFilterScope?: Scope;
  forceUpdate: Function;
  filterScope?: Scope;
  formScopingType?: ScopingType;
  chartId?: number;
  initiallyExcludedCharts?: number[];
};

const Wrapper = styled.div`
  display: flex;
  flex-direction: column;
  & > * {
    margin-bottom: ${({ theme }) => theme.gridUnit}px;
  }
`;

const CleanFormItem = styled(Form.Item)`
  margin-bottom: 0;
`;

const FilterScope: FC<FilterScopeProps> = ({
  pathToFormValue = [],
  formScopingType,
  formFilterScope,
  forceUpdate,
  filterScope,
  updateFormValues,
  chartId,
  initiallyExcludedCharts,
}) => {
  const [initialFilterScope] = useState(
    filterScope || getDefaultScopeValue(chartId, initiallyExcludedCharts),
  );
  const [initialScopingType] = useState(
    isScopingAll(initialFilterScope, chartId)
      ? ScopingType.all
      : ScopingType.specific,
  );
  const [hasScopeBeenModified, setHasScopeBeenModified] = useState(
    !!filterScope,
  );

  const onUpdateFormValues = useCallback(
    (formValues: any) => {
      updateFormValues(formValues);
      setHasScopeBeenModified(true);
    },
    [updateFormValues],
  );

  const updateScopes = useCallback(() => {
    if (filterScope || hasScopeBeenModified) {
      return;
    }

    const newScope = getDefaultScopeValue(chartId, initiallyExcludedCharts);
    updateFormValues({
      scope: newScope,
      scoping: isScopingAll(newScope, chartId)
        ? ScopingType.all
        : ScopingType.specific,
    });
  }, [
    chartId,
    filterScope,
    hasScopeBeenModified,
    initiallyExcludedCharts,
    updateFormValues,
  ]);
  useComponentDidUpdate(updateScopes);

  return (
    <Wrapper>
      <CleanFormItem
        name={[...pathToFormValue, 'scoping']}
        initialValue={initialScopingType}
      >
        <Radio.Group
          onChange={({ target: { value } }) => {
            if (value === ScopingType.all) {
              const scope = getDefaultScopeValue(chartId);
              updateFormValues({
                scope,
              });
            }
            setHasScopeBeenModified(true);
            forceUpdate();
          }}
        >
          <Radio value={ScopingType.all}>{t('Apply to all panels')}</Radio>
          <Radio value={ScopingType.specific}>
            {t('Apply to specific panels')}
          </Radio>
        </Radio.Group>
      </CleanFormItem>
      <Typography.Text type="secondary">
        {(formScopingType ?? initialScopingType) === ScopingType.specific
          ? t('Only selected panels will be affected by this filter')
          : t('All panels with this column will be affected by this filter')}
      </Typography.Text>
      {(formScopingType ?? initialScopingType) === ScopingType.specific && (
        <ScopingTree
          updateFormValues={onUpdateFormValues}
          initialScope={initialFilterScope}
          formScope={formFilterScope}
          forceUpdate={forceUpdate}
          chartId={chartId}
          initiallyExcludedCharts={initiallyExcludedCharts}
        />
      )}
      <CleanFormItem
        name={[...pathToFormValue, 'scope']}
        hidden
        initialValue={initialFilterScope}
      />
    </Wrapper>
  );
};

export default FilterScope;
