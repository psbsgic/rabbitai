import userEvent from '@testing-library/user-event';
import React from 'react';
import { render, screen } from 'spec/helpers/testing-library';
import { FilterInput } from '.';

jest.mock('lodash/debounce', () => ({
  __esModule: true,
  default: (fuc: Function) => fuc,
}));

test('Render a FilterInput', async () => {
  const onChangeHandler = jest.fn();
  render(<FilterInput onChangeHandler={onChangeHandler} />);

  expect(onChangeHandler).toBeCalledTimes(0);
  userEvent.type(screen.getByRole('textbox'), 'test');

  expect(onChangeHandler).toBeCalledTimes(4);
});
