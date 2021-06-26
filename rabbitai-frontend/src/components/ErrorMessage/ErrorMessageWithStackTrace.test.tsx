

import React from 'react';
import { render, screen } from 'spec/helpers/testing-library';
import userEvent from '@testing-library/user-event';
import ErrorMessageWithStackTrace from './ErrorMessageWithStackTrace';
import { ErrorLevel, ErrorSource } from './types';

const mockedProps = {
  level: 'warning' as ErrorLevel,
  link: 'https://sample.com',
  source: 'dashboard' as ErrorSource,
  stackTrace: 'Stacktrace',
};

test('should render', () => {
  const { container } = render(<ErrorMessageWithStackTrace {...mockedProps} />);
  expect(container).toBeInTheDocument();
});

test('should render the stacktrace', () => {
  render(<ErrorMessageWithStackTrace {...mockedProps} />, { useRedux: true });
  const button = screen.getByText('See more');
  userEvent.click(button);
  expect(screen.getByText('Stacktrace')).toBeInTheDocument();
});

test('should render the link', () => {
  render(<ErrorMessageWithStackTrace {...mockedProps} />, { useRedux: true });
  const button = screen.getByText('See more');
  userEvent.click(button);
  const link = screen.getByRole('link');
  expect(link).toHaveTextContent('(Request Access)');
  expect(link).toHaveAttribute('href', mockedProps.link);
});
