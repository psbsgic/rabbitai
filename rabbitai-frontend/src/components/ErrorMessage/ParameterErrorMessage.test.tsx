

import userEvent from '@testing-library/user-event';
import React from 'react';
import { render, screen } from 'spec/helpers/testing-library';
import ParameterErrorMessage from './ParameterErrorMessage';
import { ErrorLevel, ErrorSource, ErrorTypeEnum } from './types';

const mockedProps = {
  error: {
    error_type: ErrorTypeEnum.MISSING_TEMPLATE_PARAMS_ERROR,
    extra: {
      template_parameters: { state: 'CA', country: 'ITA' },
      undefined_parameters: ['stat', 'count'],
      issue_codes: [
        {
          code: 1,
          message: 'Issue code message A',
        },
        {
          code: 2,
          message: 'Issue code message B',
        },
      ],
    },
    level: 'error' as ErrorLevel,
    message: 'Error message',
  },
  source: 'dashboard' as ErrorSource,
};

test('should render', () => {
  const { container } = render(<ParameterErrorMessage {...mockedProps} />);
  expect(container).toBeInTheDocument();
});

test('should render the default title', () => {
  render(<ParameterErrorMessage {...mockedProps} />);
  expect(screen.getByText('Parameter error')).toBeInTheDocument();
});

test('should render the error message', () => {
  render(<ParameterErrorMessage {...mockedProps} />, { useRedux: true });
  const button = screen.getByText('See more');
  userEvent.click(button);
  expect(screen.getByText('Error message')).toBeInTheDocument();
});

test('should render the issue codes', () => {
  render(<ParameterErrorMessage {...mockedProps} />, { useRedux: true });
  const button = screen.getByText('See more');
  userEvent.click(button);
  expect(screen.getByText(/This may be triggered by:/)).toBeInTheDocument();
  expect(screen.getByText(/Issue code message A/)).toBeInTheDocument();
  expect(screen.getByText(/Issue code message B/)).toBeInTheDocument();
});

test('should render the suggestions', () => {
  render(<ParameterErrorMessage {...mockedProps} />, { useRedux: true });
  const button = screen.getByText('See more');
  userEvent.click(button);
  expect(screen.getByText(/Did you mean:/)).toBeInTheDocument();
  expect(screen.getByText('"state" instead of "stat?"')).toBeInTheDocument();
  expect(screen.getByText('"country" instead of "count?"')).toBeInTheDocument();
});
