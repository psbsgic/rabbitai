import React from 'react';
import moment from 'moment-timezone';
import { render } from 'spec/helpers/testing-library';
import TimezoneSelector from './index';

describe('TimezoneSelector', () => {
  let timezone: string;
  const onTimezoneChange = jest.fn(zone => {
    timezone = zone;
  });
  it('renders a TimezoneSelector with a default if undefined', () => {
    jest.spyOn(moment.tz, 'guess').mockReturnValue('America/New_York');
    render(
      <TimezoneSelector
        onTimezoneChange={onTimezoneChange}
        timezone={timezone}
      />,
    );
    expect(onTimezoneChange).toHaveBeenCalledWith('America/Nassau');
  });
  it('renders a TimezoneSelector with the closest value if passed in', async () => {
    render(
      <TimezoneSelector
        onTimezoneChange={onTimezoneChange}
        timezone="America/Los_Angeles"
      />,
    );
    expect(onTimezoneChange).toHaveBeenLastCalledWith('America/Vancouver');
  });
});
