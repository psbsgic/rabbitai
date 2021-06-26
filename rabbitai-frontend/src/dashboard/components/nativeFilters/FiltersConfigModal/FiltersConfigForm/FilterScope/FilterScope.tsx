

import React, { FC } from 'react';
import { t, styled } from '@rabbitai-ui/core';
import { Radio } from 'src/components/Radio';
import { Form, Typography } from 'src/common/components';
import { Scope } from '../../../types';
import { Scoping } from './types';
import ScopingTree from './ScopingTree';
import { getDefaultScopeValue, isScopingAll } from './utils';

type FilterScopeProps = {
  pathToFormValue?: string[];
  updateFormValues: (values: any) => void;
  formScope?: Scope;
  forceUpdate: Function;
  scope?: Scope;
  formScoping?: Scoping;
  chartId?: number;
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
  formScoping,
  formScope,
  forceUpdate,
  scope,
  updateFormValues,
  chartId,
}) => {
  const initialScope = scope || getDefaultScopeValue(chartId);
  const initialScoping = isScopingAll(initialScope, chartId)
    ? Scoping.all
    : Scoping.specific;

  return (
    <Wrapper>
      <CleanFormItem
        name={[...pathToFormValue, 'scoping']}
        initialValue={initialScoping}
      >
        <Radio.Group
          onChange={({ target: { value } }) => {
            if (value === Scoping.all) {
              const scope = getDefaultScopeValue(chartId);
              updateFormValues({
                scope,
              });
            }
            forceUpdate();
          }}
        >
          <Radio value={Scoping.all}>{t('Apply to all panels')}</Radio>
          <Radio value={Scoping.specific}>
            {t('Apply to specific panels')}
          </Radio>
        </Radio.Group>
      </CleanFormItem>
      <Typography.Text type="secondary">
        {(formScoping ?? initialScoping) === Scoping.specific
          ? t('Only selected panels will be affected by this filter')
          : t('All panels with this column will be affected by this filter')}
      </Typography.Text>
      {(formScoping ?? initialScoping) === Scoping.specific && (
        <ScopingTree
          updateFormValues={updateFormValues}
          initialScope={initialScope}
          formScope={formScope}
          forceUpdate={forceUpdate}
          chartId={chartId}
        />
      )}
      <CleanFormItem
        name={[...pathToFormValue, 'scope']}
        hidden
        initialValue={initialScope}
      />
    </Wrapper>
  );
};

export default FilterScope;
