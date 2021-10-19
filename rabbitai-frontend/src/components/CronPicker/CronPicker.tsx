import React from 'react';
import { ConfigProvider } from 'antd';
import { styled, t } from '@superset-ui/core';
import ReactCronPicker, { Locale, CronProps } from 'react-js-cron';

export * from 'react-js-cron';

export const LOCALE: Locale = {
  everyText: t('every'),
  emptyMonths: t('every month'),
  emptyMonthDays: t('every day of the month'),
  emptyMonthDaysShort: t('day of the month'),
  emptyWeekDays: t('every day of the week'),
  emptyWeekDaysShort: t('day of the week'),
  emptyHours: t('every hour'),
  emptyMinutes: t('every minute'),
  emptyMinutesForHourPeriod: t('every'),
  yearOption: t('year'),
  monthOption: t('month'),
  weekOption: t('week'),
  dayOption: t('day'),
  hourOption: t('hour'),
  minuteOption: t('minute'),
  rebootOption: t('reboot'),
  prefixPeriod: t('Every'),
  prefixMonths: t('in'),
  prefixMonthDays: t('on'),
  prefixWeekDays: t('on'),
  prefixWeekDaysForMonthAndYearPeriod: t('and'),
  prefixHours: t('at'),
  prefixMinutes: t(':'),
  prefixMinutesForHourPeriod: t('at'),
  suffixMinutesForHourPeriod: t('minute(s)'),
  errorInvalidCron: t('Invalid cron expression'),
  clearButtonText: t('Clear'),
  weekDays: [
    // Order is important, the index will be used as value
    t('Sunday'), // Sunday must always be first, it's "0"
    t('Monday'),
    t('Tuesday'),
    t('Wednesday'),
    t('Thursday'),
    t('Friday'),
    t('Saturday'),
  ],
  months: [
    // Order is important, the index will be used as value
    t('January'),
    t('February'),
    t('March'),
    t('April'),
    t('May'),
    t('June'),
    t('July'),
    t('August'),
    t('September'),
    t('October'),
    t('November'),
    t('December'),
  ],
  // Order is important, the index will be used as value
  altWeekDays: [
    t('SUN'), // Sunday must always be first, it's "0"
    t('MON'),
    t('TUE'),
    t('WED'),
    t('THU'),
    t('FRI'),
    t('SAT'),
  ],
  // Order is important, the index will be used as value
  altMonths: [
    t('JAN'),
    t('FEB'),
    t('MAR'),
    t('APR'),
    t('MAY'),
    t('JUN'),
    t('JUL'),
    t('AUG'),
    t('SEP'),
    t('OCT'),
    t('NOV'),
    t('DEC'),
  ],
};

export const CronPicker = styled((props: CronProps) => (
  <ConfigProvider
    getPopupContainer={trigger => trigger.parentElement as HTMLElement}
  >
    <ReactCronPicker locale={LOCALE} {...props} />
  </ConfigProvider>
))`
  .react-js-cron-select:not(.react-js-cron-custom-select) > div:first-of-type,
  .react-js-cron-custom-select {
    border-radius: ${({ theme }) => theme.gridUnit}px;
    background-color: ${({ theme }) =>
      theme.colors.grayscale.light4} !important;
  }
  .react-js-cron-custom-select > div:first-of-type {
    border-radius: ${({ theme }) => theme.gridUnit}px;
  }
`;
