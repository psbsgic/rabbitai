

import React from 'react';
import { render, screen } from 'spec/helpers/testing-library';
import { rabbitaiTheme } from '@rabbitai-ui/core';
import BasicErrorAlert from './BasicErrorAlert';
import { ErrorLevel } from './types';

const mockedProps = {
  body: 'Error body',
  level: 'warning' as ErrorLevel,
  title: 'Error title',
};

jest.mock('../Icon', () => ({
  __esModule: true,
  default: ({ name }: { name: string }) => (
    <div data-test="icon" data-name={name} />
  ),
}));

test('should render', () => {
  const { container } = render(<BasicErrorAlert {...mockedProps} />);
  expect(container).toBeInTheDocument();
});

test('should render warning icon', () => {
  render(<BasicErrorAlert {...mockedProps} />);
  expect(screen.getByTestId('icon')).toBeInTheDocument();
  expect(screen.getByTestId('icon')).toHaveAttribute(
    'data-name',
    'warning-solid',
  );
});

test('should render error icon', () => {
  const errorProps = {
    ...mockedProps,
    level: 'error' as ErrorLevel,
  };
  render(<BasicErrorAlert {...errorProps} />);
  expect(screen.getByTestId('icon')).toBeInTheDocument();
  expect(screen.getByTestId('icon')).toHaveAttribute(
    'data-name',
    'error-solid',
  );
});

test('should render the error title', () => {
  render(<BasicErrorAlert {...mockedProps} />);
  expect(screen.getByText('Error title')).toBeInTheDocument();
});

test('should render the error body', () => {
  render(<BasicErrorAlert {...mockedProps} />);
  expect(screen.getByText('Error body')).toBeInTheDocument();
});

test('should render with warning theme', () => {
  render(<BasicErrorAlert {...mockedProps} />);
  expect(screen.getByRole('alert')).toHaveStyle(
    `
      backgroundColor: ${rabbitaiTheme.colors.warning.light2};
    `,
  );
});

test('should render with error theme', () => {
  const errorProps = {
    ...mockedProps,
    level: 'error' as ErrorLevel,
  };
  render(<BasicErrorAlert {...errorProps} />);
  expect(screen.getByRole('alert')).toHaveStyle(
    `
      backgroundColor: ${rabbitaiTheme.colors.error.light2};
    `,
  );
});
