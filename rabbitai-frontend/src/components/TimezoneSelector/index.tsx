import React, { useEffect, useRef } from 'react';
import moment from 'moment-timezone';

import { NativeGraySelect as Select } from 'src/components/Select';

const DEFAULT_TIMEZONE = 'GMT Standard Time';
const MIN_SELECT_WIDTH = '400px';

const offsetsToName = {
  '-300-240': ['Eastern Standard Time', 'Eastern Daylight Time'],
  '-360-300': ['Central Standard Time', 'Central Daylight Time'],
  '-420-360': ['Mountain Standard Time', 'Mountain Daylight Time'],
  '-420-420': [
    'Mountain Standard Time - Phoenix',
    'Mountain Standard Time - Phoenix',
  ],
  '-480-420': ['Pacific Standard Time', 'Pacific Daylight Time'],
  '-540-480': ['Alaska Standard Time', 'Alaska Daylight Time'],
  '-600-600': ['Hawaii Standard Time', 'Hawaii Daylight Time'],
  '60120': ['Central European Time', 'Central European Daylight Time'],
  '00': [DEFAULT_TIMEZONE, DEFAULT_TIMEZONE],
  '060': ['GMT Standard Time - London', 'British Summer Time'],
};

const currentDate = moment();
const JANUARY = moment([2021, 1]);
const JULY = moment([2021, 7]);

const getOffsetKey = (name: string) =>
  JANUARY.tz(name).utcOffset().toString() +
  JULY.tz(name).utcOffset().toString();

const getTimezoneName = (name: string) => {
  const offsets = getOffsetKey(name);
  return (
    (currentDate.tz(name).isDST()
      ? offsetsToName[offsets]?.[1]
      : offsetsToName[offsets]?.[0]) || name
  );
};

export interface TimezoneProps {
  onTimezoneChange: (value: string) => void;
  timezone?: string | null;
}

const ALL_ZONES = moment.tz
  .countries()
  .map(country => moment.tz.zonesForCountry(country, true))
  .flat();

const TIMEZONES: moment.MomentZoneOffset[] = [];
ALL_ZONES.forEach(zone => {
  if (
    !TIMEZONES.find(
      option => getOffsetKey(option.name) === getOffsetKey(zone.name),
    )
  ) {
    TIMEZONES.push(zone); // dedupe zones by offsets
  }
});

const TIMEZONE_OPTIONS = TIMEZONES.sort(
  // sort by offset
  (a, b) =>
    moment.tz(currentDate, a.name).utcOffset() -
    moment.tz(currentDate, b.name).utcOffset(),
).map(zone => ({
  label: `GMT ${moment
    .tz(currentDate, zone.name)
    .format('Z')} (${getTimezoneName(zone.name)})`,
  value: zone.name,
  offsets: getOffsetKey(zone.name),
}));

const timezoneOptions = TIMEZONE_OPTIONS.map(option => (
  <Select.Option key={option.value} value={option.value}>
    {option.label}
  </Select.Option>
));

const TimezoneSelector = ({ onTimezoneChange, timezone }: TimezoneProps) => {
  const prevTimezone = useRef(timezone);
  const matchTimezoneToOptions = (timezone: string) =>
    TIMEZONE_OPTIONS.find(option => option.offsets === getOffsetKey(timezone))
      ?.value || DEFAULT_TIMEZONE;

  const updateTimezone = (tz: string) => {
    // update the ref to track changes
    prevTimezone.current = tz;
    // the parent component contains the state for the value
    onTimezoneChange(tz);
  };

  useEffect(() => {
    const updatedTz = matchTimezoneToOptions(timezone || moment.tz.guess());
    if (prevTimezone.current !== updatedTz) {
      updateTimezone(updatedTz);
    }
  }, [timezone]);

  return (
    <Select
      css={{ minWidth: MIN_SELECT_WIDTH }} // smallest size for current values
      onChange={onTimezoneChange}
      value={timezone || DEFAULT_TIMEZONE}
    >
      {timezoneOptions}
    </Select>
  );
};

export default TimezoneSelector;
