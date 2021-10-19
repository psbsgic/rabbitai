export type SelectOptionType = {
  value: string;
  label: string;
};

export type FrameType =
  | 'Common'
  | 'Calendar'
  | 'Custom'
  | 'Advanced'
  | 'No filter';

export type DateTimeGrainType =
  | 'second'
  | 'minite'
  | 'hour'
  | 'day'
  | 'week'
  | 'month'
  | 'quarter'
  | 'year';

export type CustomRangeKey =
  | 'sinceMode'
  | 'sinceDatetime'
  | 'sinceGrain'
  | 'sinceGrainValue'
  | 'untilMode'
  | 'untilDatetime'
  | 'untilGrain'
  | 'untilGrainValue'
  | 'anchorMode'
  | 'anchorValue';

export type DateTimeModeType = 'specific' | 'relative' | 'now' | 'today';

export type CustomRangeType = {
  sinceMode: DateTimeModeType;
  sinceDatetime: string;
  sinceGrain: DateTimeGrainType;
  sinceGrainValue: number;
  untilMode: DateTimeModeType;
  untilDatetime: string;
  untilGrain: DateTimeGrainType;
  untilGrainValue: number;
  anchorMode: 'now' | 'specific';
  anchorValue: string;
};

export type CustomRangeDecodeType = {
  customRange: CustomRangeType;
  matchedFlag: boolean;
};

export type CommonRangeType =
  | 'Last day'
  | 'Last week'
  | 'Last month'
  | 'Last quarter'
  | 'Last year';

export const PreviousCalendarWeek = 'previous calendar week';
export const PreviousCalendarMonth = 'previous calendar month';
export const PreviousCalendarYear = 'previous calendar year';
export type CalendarRangeType =
  | typeof PreviousCalendarWeek
  | typeof PreviousCalendarMonth
  | typeof PreviousCalendarYear;

export type FrameComponentProps = {
  onChange: (timeRange: string) => void;
  value: string;
};
