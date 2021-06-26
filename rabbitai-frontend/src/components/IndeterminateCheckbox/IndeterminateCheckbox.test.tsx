

import React from 'react';
import { render, screen } from 'spec/helpers/testing-library';
import userEvent from '@testing-library/user-event';
import IndeterminateCheckbox from '.';

const mockedProps = {
  checked: false,
  id: 'checkbox-id',
  indeterminate: false,
  title: 'Checkbox title',
  onChange: jest.fn(),
};

test('should render', () => {
  const { container } = render(<IndeterminateCheckbox {...mockedProps} />);
  expect(container).toBeInTheDocument();
});

test('should render the label', () => {
  render(<IndeterminateCheckbox {...mockedProps} />);
  expect(screen.getByTitle('Checkbox title')).toBeInTheDocument();
});

test('should render the checkbox', () => {
  render(<IndeterminateCheckbox {...mockedProps} />);
  expect(screen.getByRole('checkbox')).toBeInTheDocument();
});

test('should render the checkbox-half icon', () => {
  const indeterminateProps = {
    ...mockedProps,
    indeterminate: true,
  };
  render(<IndeterminateCheckbox {...indeterminateProps} />);
  expect(screen.getByRole('img')).toBeInTheDocument();
  expect(screen.getByRole('img')).toHaveAttribute(
    'aria-label',
    'checkbox-half',
  );
});

test('should render the checkbox-off icon', () => {
  render(<IndeterminateCheckbox {...mockedProps} />);
  expect(screen.getByRole('img')).toBeInTheDocument();
  expect(screen.getByRole('img')).toHaveAttribute('aria-label', 'checkbox-off');
});

test('should render the checkbox-on icon', () => {
  const checkboxOnProps = {
    ...mockedProps,
    checked: true,
  };
  render(<IndeterminateCheckbox {...checkboxOnProps} />);
  expect(screen.getByRole('img')).toBeInTheDocument();
  expect(screen.getByRole('img')).toHaveAttribute('aria-label', 'checkbox-on');
});

test('should call the onChange', () => {
  render(<IndeterminateCheckbox {...mockedProps} />);
  const label = screen.getByTitle('Checkbox title');
  userEvent.click(label);
  expect(mockedProps.onChange).toHaveBeenCalledTimes(1);
});
