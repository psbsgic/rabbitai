

import React from 'react';
import { render, screen } from 'spec/helpers/testing-library';
import userEvent from '@testing-library/user-event';
import { Ellipsis } from './Ellipsis';

test('Ellipsis - click when the button is enabled', () => {
  const click = jest.fn();
  render(<Ellipsis onClick={click} />);
  expect(click).toBeCalledTimes(0);
  userEvent.click(screen.getByRole('button'));
  expect(click).toBeCalledTimes(1);
});

test('Ellipsis - click when the button is disabled', () => {
  const click = jest.fn();
  render(<Ellipsis onClick={click} disabled />);
  expect(click).toBeCalledTimes(0);
  userEvent.click(screen.getByRole('button'));
  expect(click).toBeCalledTimes(0);
});
