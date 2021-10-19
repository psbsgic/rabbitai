import React from 'react';
import { render, screen } from 'spec/helpers/testing-library';
import userEvent from '@testing-library/user-event';
import { Item } from './Item';

test('Item - click when the item is not active', () => {
  const click = jest.fn();
  render(
    <Item onClick={click}>
      <div data-test="test" />
    </Item>,
  );
  expect(click).toBeCalledTimes(0);
  userEvent.click(screen.getByRole('button'));
  expect(click).toBeCalledTimes(1);
  expect(screen.getByTestId('test')).toBeInTheDocument();
});

test('Item - click when the item is active', () => {
  const click = jest.fn();
  render(
    <Item onClick={click} active>
      <div data-test="test" />
    </Item>,
  );
  expect(click).toBeCalledTimes(0);
  userEvent.click(screen.getByRole('button'));
  expect(click).toBeCalledTimes(0);
  expect(screen.getByTestId('test')).toBeInTheDocument();
});
