import React from 'react';
import { render, screen } from 'spec/helpers/testing-library';
import { DndItemType } from 'src/explore/components/DndItemType';
import DndSelectLabel from 'src/explore/components/controls/DndColumnSelectControl/DndSelectLabel';

const defaultProps = {
  name: 'Column',
  accept: 'Column' as DndItemType,
  onDrop: jest.fn(),
  canDrop: () => false,
  valuesRenderer: () => <span />,
  onChange: jest.fn(),
  options: { string: { column_name: 'Column' } },
};

test('renders with default props', async () => {
  render(<DndSelectLabel {...defaultProps} />, { useDnd: true });
  expect(await screen.findByText('Drop columns here')).toBeInTheDocument();
});

test('renders ghost button when empty', async () => {
  const ghostButtonText = 'Ghost button text';
  render(
    <DndSelectLabel {...defaultProps} ghostButtonText={ghostButtonText} />,
    { useDnd: true },
  );
  expect(await screen.findByText(ghostButtonText)).toBeInTheDocument();
});

test('renders values', async () => {
  const values = 'Values';
  const valuesRenderer = () => <span>{values}</span>;
  render(<DndSelectLabel {...defaultProps} valuesRenderer={valuesRenderer} />, {
    useDnd: true,
  });
  expect(await screen.findByText(values)).toBeInTheDocument();
});
