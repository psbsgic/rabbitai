import React from 'react';
import { render, screen } from 'spec/helpers/testing-library';
import { RowCount } from '.';

test('Render a RowCount', () => {
  render(<RowCount data={[{}, {}, {}]} loading={false} />);
  expect(screen.getByText('3 rows retrieved')).toBeInTheDocument();
});

test('Render a RowCount on loading', () => {
  render(<RowCount data={[{}, {}, {}]} loading />);
  expect(screen.getByText('Loading...')).toBeInTheDocument();
});
