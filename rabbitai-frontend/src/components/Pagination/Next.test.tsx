

import React from 'react';
import { render, screen } from 'spec/helpers/testing-library';
import userEvent from '@testing-library/user-event';
import { Next } from './Next';

test('Next - click when the button is enabled', () => {
  const click = jest.fn();
  render(<Next onClick={click} />);
  expect(click).toBeCalledTimes(0);
  userEvent.click(screen.getByRole('button'));
  expect(click).toBeCalledTimes(1);
});

test('Next - click when the button is disabled', () => {
  const click = jest.fn();
  render(<Next onClick={click} disabled />);
  expect(click).toBeCalledTimes(0);
  userEvent.click(screen.getByRole('button'));
  expect(click).toBeCalledTimes(0);
});
