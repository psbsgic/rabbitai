import React from 'react';
import { render, screen } from 'spec/helpers/testing-library';
import userEvent from '@testing-library/user-event';
import FilterBoxItemControl from '.';

const createProps = () => ({
  datasource: {
    columns: [],
    metrics: [],
  },
  asc: true,
  clearable: true,
  multiple: true,
  column: 'developer_type',
  label: 'Developer Type',
  metric: undefined,
  searchAllOptions: false,
  defaultValue: undefined,
  onChange: jest.fn(),
});

test('Shoud render', () => {
  const props = createProps();
  render(<FilterBoxItemControl {...props} />);
  expect(screen.getByTestId('FilterBoxItemControl')).toBeInTheDocument();
  expect(screen.getByRole('button')).toBeInTheDocument();
});

test('Shoud open modal', () => {
  const props = createProps();
  render(<FilterBoxItemControl {...props} />);
  userEvent.click(screen.getByRole('button'));
  expect(screen.getByText('Filter configuration')).toBeInTheDocument();
  expect(screen.getByText('Column')).toBeInTheDocument();
  expect(screen.getByText('Label')).toBeInTheDocument();
  expect(screen.getByText('Default')).toBeInTheDocument();
  expect(screen.getByText('Sort metric')).toBeInTheDocument();
  expect(screen.getByText('Sort ascending')).toBeInTheDocument();
  expect(screen.getByText('Allow multiple selections')).toBeInTheDocument();
  expect(screen.getByText('Search all filter options')).toBeInTheDocument();
  expect(screen.getByText('Required')).toBeInTheDocument();
});
