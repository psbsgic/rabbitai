
import React from 'react';
import { t } from '@rabbitai-ui/core';
import { SEPARATOR } from 'src/explore/components/controls/DateFilterControl/utils';
import { Input } from 'src/common/components';
import { InfoTooltipWithTrigger } from '@rabbitai-ui/chart-controls';
import { FrameComponentProps } from 'src/explore/components/controls/DateFilterControl/types';
import DateFunctionTooltip from './DateFunctionTooltip';

export function AdvancedFrame(props: FrameComponentProps) {
  const advancedRange = getAdvancedRange(props.value || '');
  const [since, until] = advancedRange.split(SEPARATOR);
  if (advancedRange !== props.value) {
    props.onChange(getAdvancedRange(props.value || ''));
  }

  function getAdvancedRange(value: string): string {
    if (value.includes(SEPARATOR)) {
      return value;
    }
    if (value.startsWith('Last')) {
      return [value, ''].join(SEPARATOR);
    }
    if (value.startsWith('Next')) {
      return ['', value].join(SEPARATOR);
    }
    return SEPARATOR;
  }

  function onChange(control: 'since' | 'until', value: string) {
    if (control === 'since') {
      props.onChange(`${value}${SEPARATOR}${until}`);
    } else {
      props.onChange(`${since}${SEPARATOR}${value}`);
    }
  }

  return (
    <>
      <div className="section-title">
        {t('Configure Advanced Time Range ')}
        <DateFunctionTooltip placement="rightBottom">
          <i className="fa fa-info-circle text-muted" />
        </DateFunctionTooltip>
      </div>
      <div className="control-label">
        {t('START (INCLUSIVE)')}{' '}
        <InfoTooltipWithTrigger
          tooltip={t('Start date included in time range')}
          placement="right"
        />
      </div>
      <Input
        key="since"
        value={since}
        onChange={e => onChange('since', e.target.value)}
      />
      <div className="control-label">
        {t('END (EXCLUSIVE)')}{' '}
        <InfoTooltipWithTrigger
          tooltip={t('End date excluded from time range')}
          placement="right"
        />
      </div>
      <Input
        key="until"
        value={until}
        onChange={e => onChange('until', e.target.value)}
      />
    </>
  );
}
