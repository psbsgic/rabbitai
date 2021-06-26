
import React from 'react';
import { GenericDataType } from '@rabbitai-ui/core';
import { render, screen } from 'spec/helpers/testing-library';
import AdhocMetric from 'src/explore/components/controls/MetricControl/AdhocMetric';
import AdhocFilter, {
  EXPRESSION_TYPES,
} from 'src/explore/components/controls/FilterControl/AdhocFilter';
import { DndFilterSelect } from 'src/explore/components/controls/DndColumnSelectControl/DndFilterSelect';

const defaultProps = {
  name: 'Filter',
  value: [],
  columns: [],
  datasource: {},
  formData: {},
  savedMetrics: [],
  onChange: jest.fn(),
  options: { string: { column_name: 'Column' } },
};

test('renders with default props', () => {
  render(<DndFilterSelect {...defaultProps} />, { useDnd: true });
  expect(screen.getByText('Drop columns or metrics')).toBeInTheDocument();
});

test('renders with value', () => {
  const value = new AdhocFilter({
    sqlExpression: 'COUNT(*)',
    expressionType: EXPRESSION_TYPES.SQL,
  });
  render(<DndFilterSelect {...defaultProps} value={[value]} />, {
    useDnd: true,
  });
  expect(screen.getByText('COUNT(*)')).toBeInTheDocument();
});

test('renders options with saved metric', () => {
  render(<DndFilterSelect {...defaultProps} formData={['saved_metric']} />, {
    useDnd: true,
  });
  expect(screen.getByText('Drop columns or metrics')).toBeInTheDocument();
});

test('renders options with column', () => {
  render(
    <DndFilterSelect
      {...defaultProps}
      columns={[
        {
          id: 1,
          type: 'VARCHAR',
          type_generic: GenericDataType.STRING,
          column_name: 'Column',
        },
      ]}
    />,
    {
      useDnd: true,
    },
  );
  expect(screen.getByText('Drop columns or metrics')).toBeInTheDocument();
});

test('renders options with adhoc metric', () => {
  const adhocMetric = new AdhocMetric({
    expression: 'AVG(birth_names.num)',
    metric_name: 'avg__num',
  });
  render(<DndFilterSelect {...defaultProps} formData={[adhocMetric]} />, {
    useDnd: true,
  });
  expect(screen.getByText('Drop columns or metrics')).toBeInTheDocument();
});
