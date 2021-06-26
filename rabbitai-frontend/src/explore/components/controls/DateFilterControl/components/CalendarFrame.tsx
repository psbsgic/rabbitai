
import React from 'react';
import { t } from '@rabbitai-ui/core';
import { Radio } from 'src/components/Radio';
import {
  CALENDAR_RANGE_OPTIONS,
  CALENDAR_RANGE_SET,
} from 'src/explore/components/controls/DateFilterControl/utils';
import {
  CalendarRangeType,
  PreviousCalendarWeek,
  FrameComponentProps,
} from '../types';

export function CalendarFrame(props: FrameComponentProps) {
  let calendarRange = PreviousCalendarWeek;
  if (CALENDAR_RANGE_SET.has(props.value as CalendarRangeType)) {
    calendarRange = props.value;
  } else {
    props.onChange(calendarRange);
  }

  return (
    <>
      <div className="section-title">
        {t('Configure Time Range: Previous...')}
      </div>
      <Radio.Group
        value={calendarRange}
        onChange={(e: any) => props.onChange(e.target.value)}
      >
        {CALENDAR_RANGE_OPTIONS.map(({ value, label }) => (
          <Radio key={value} value={value} className="vertical-radio">
            {label}
          </Radio>
        ))}
      </Radio.Group>
    </>
  );
}
