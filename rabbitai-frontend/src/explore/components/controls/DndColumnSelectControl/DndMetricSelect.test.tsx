
import React from 'react';
import { render, screen } from 'spec/helpers/testing-library';
import { DndMetricSelect } from 'src/explore/components/controls/DndColumnSelectControl/DndMetricSelect';

const defaultProps = {
  savedMetrics: [
    {
      metric_name: 'Metric A',
      expression: 'Expression A',
    },
  ],
};

test('renders with default props', () => {
  render(<DndMetricSelect {...defaultProps} />, { useDnd: true });
  expect(screen.getByText('Drop column or metric')).toBeInTheDocument();
});

test('renders with default props and multi = true', () => {
  render(<DndMetricSelect {...defaultProps} multi />, { useDnd: true });
  expect(screen.getByText('Drop columns or metrics')).toBeInTheDocument();
});
