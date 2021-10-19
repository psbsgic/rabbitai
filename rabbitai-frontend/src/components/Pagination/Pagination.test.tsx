import React from 'react';
import { render, screen } from 'spec/helpers/testing-library';
import Pagination from '.';

jest.mock('./Next', () => ({
  Next: () => <div data-test="next" />,
}));
jest.mock('./Prev', () => ({
  Prev: () => <div data-test="prev" />,
}));
jest.mock('./Item', () => ({
  Item: () => <div data-test="item" />,
}));
jest.mock('./Ellipsis', () => ({
  Ellipsis: () => <div data-test="ellipsis" />,
}));

test('Pagination rendering correctly', () => {
  render(
    <Pagination>
      <li data-test="test" />
    </Pagination>,
  );
  expect(screen.getByRole('navigation')).toBeInTheDocument();
  expect(screen.getByTestId('test')).toBeInTheDocument();
});

test('Next attribute', () => {
  render(<Pagination.Next onClick={jest.fn()} />);
  expect(screen.getByTestId('next')).toBeInTheDocument();
});

test('Prev attribute', () => {
  render(<Pagination.Next onClick={jest.fn()} />);
  expect(screen.getByTestId('next')).toBeInTheDocument();
});

test('Item attribute', () => {
  render(
    <Pagination.Item onClick={jest.fn()}>
      <></>
    </Pagination.Item>,
  );
  expect(screen.getByTestId('item')).toBeInTheDocument();
});

test('Ellipsis attribute', () => {
  render(<Pagination.Ellipsis onClick={jest.fn()} />);
  expect(screen.getByTestId('ellipsis')).toBeInTheDocument();
});
