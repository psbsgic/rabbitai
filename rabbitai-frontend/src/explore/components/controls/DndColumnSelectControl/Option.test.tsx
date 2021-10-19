import React from 'react';
import { render, screen } from 'spec/helpers/testing-library';
import userEvent from '@testing-library/user-event';
import Option from 'src/explore/components/controls/DndColumnSelectControl/Option';

test('renders with default props', () => {
  const { container } = render(
    <Option index={1} clickClose={jest.fn()}>
      Option
    </Option>,
  );
  expect(container).toBeInTheDocument();
  expect(screen.getByRole('img', { name: 'x-small' })).toBeInTheDocument();
  expect(
    screen.queryByRole('img', { name: 'caret-right' }),
  ).not.toBeInTheDocument();
});

test('renders with caret', () => {
  render(
    <Option index={1} clickClose={jest.fn()} withCaret>
      Option
    </Option>,
  );
  expect(screen.getByRole('img', { name: 'x-small' })).toBeInTheDocument();
  expect(screen.getByRole('img', { name: 'caret-right' })).toBeInTheDocument();
});

test('renders with extra triangle', () => {
  render(
    <Option index={1} clickClose={jest.fn()} isExtra>
      Option
    </Option>,
  );
  expect(
    screen.getByRole('button', { name: 'Show info tooltip' }),
  ).toBeInTheDocument();
});

test('triggers onClose', () => {
  const clickClose = jest.fn();
  render(
    <Option index={1} clickClose={clickClose}>
      Option
    </Option>,
  );
  userEvent.click(screen.getByRole('img', { name: 'x-small' }));
  expect(clickClose).toHaveBeenCalled();
});
