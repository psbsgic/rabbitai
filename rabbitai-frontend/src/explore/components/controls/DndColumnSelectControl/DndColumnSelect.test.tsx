
import React from 'react';
import { render, screen } from 'spec/helpers/testing-library';
import { LabelProps } from 'src/explore/components/controls/DndColumnSelectControl/types';
import { DndColumnSelect } from 'src/explore/components/controls/DndColumnSelectControl/DndColumnSelect';

const defaultProps: LabelProps = {
  name: 'Filter',
  onChange: jest.fn(),
  options: { string: { column_name: 'Column A' } },
};

test('renders with default props', () => {
  render(<DndColumnSelect {...defaultProps} />, { useDnd: true });
  expect(screen.getByText('Drop columns')).toBeInTheDocument();
});

test('renders with value', () => {
  render(<DndColumnSelect {...defaultProps} value="string" />, {
    useDnd: true,
  });
  expect(screen.getByText('Column A')).toBeInTheDocument();
});
