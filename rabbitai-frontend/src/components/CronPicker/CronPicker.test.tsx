

import React from 'react';
import { render } from 'spec/helpers/testing-library';
import * as ReactCronPicker from 'react-js-cron';
import { CronPicker } from './CronPicker';

const spy = jest.spyOn(ReactCronPicker, 'default');

test('Should send correct props to ReactCronPicker', () => {
  const props = {
    myCustomProp: 'myCustomProp',
  };
  render(<CronPicker {...(props as any)} />);
  expect(spy).toBeCalledWith(
    expect.objectContaining({
      className: expect.any(String),
      locale: expect.anything(),
      myCustomProp: 'myCustomProp',
    }),
    expect.anything(),
  );
});
