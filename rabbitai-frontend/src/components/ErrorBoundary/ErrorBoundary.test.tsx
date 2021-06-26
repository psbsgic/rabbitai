
import React from 'react';
import { render, screen } from 'spec/helpers/testing-library';
import ErrorBoundary from '.';

const mockedProps = {
  children: <span>Error children</span>,
  onError: () => null,
  showMessage: false,
};

const Child = () => {
  throw new Error('Thrown error');
};

test('should render', () => {
  const { container } = render(
    <ErrorBoundary {...mockedProps}>
      <Child />
    </ErrorBoundary>,
  );
  expect(container).toBeInTheDocument();
});

test('should not render an error message', () => {
  render(
    <ErrorBoundary {...mockedProps}>
      <Child />
    </ErrorBoundary>,
  );
  expect(screen.queryByText('Unexpected error')).not.toBeInTheDocument();
});

test('should render an error message', () => {
  const messageProps = {
    ...mockedProps,
    showMessage: true,
  };
  render(
    <ErrorBoundary {...messageProps}>
      <Child />
    </ErrorBoundary>,
  );
  expect(screen.getByText('Unexpected error')).toBeInTheDocument();
});
