
import React from 'react';
import { render, screen } from 'spec/helpers/testing-library';
import userEvent from '@testing-library/user-event';
import AdhocFilter, {
  EXPRESSION_TYPES,
  CLAUSES,
} from 'src/explore/components/controls/FilterControl/AdhocFilter';
import AdhocFilterPopoverTrigger from '.';

const simpleAdhocFilter = new AdhocFilter({
  expressionType: EXPRESSION_TYPES.SIMPLE,
  subject: 'value',
  operator: '>',
  comparator: '10',
  clause: CLAUSES.WHERE,
});

const mockedProps = {
  adhocFilter: simpleAdhocFilter,
  options: [],
  datasource: {},
  onFilterEdit: jest.fn(),
};

test('should render', () => {
  const { container } = render(
    <AdhocFilterPopoverTrigger {...mockedProps}>
      Click
    </AdhocFilterPopoverTrigger>,
  );
  expect(container).toBeInTheDocument();
});

test('should render the Popover on click when uncontrolled', () => {
  render(
    <AdhocFilterPopoverTrigger {...mockedProps}>
      Click
    </AdhocFilterPopoverTrigger>,
  );
  expect(screen.queryByRole('tooltip')).not.toBeInTheDocument();
  userEvent.click(screen.getByText('Click'));
  expect(screen.getByRole('tooltip')).toBeInTheDocument();
});

test('should be visible when controlled', async () => {
  const controlledProps = {
    ...mockedProps,
    isControlledComponent: true,
    visible: true,
    togglePopover: jest.fn(),
    closePopover: jest.fn(),
  };
  render(
    <AdhocFilterPopoverTrigger {...controlledProps}>
      Click
    </AdhocFilterPopoverTrigger>,
  );
  expect(screen.getByRole('tooltip')).toBeInTheDocument();
});

test('should NOT be visible when controlled', () => {
  const controlledProps = {
    ...mockedProps,
    isControlledComponent: true,
    visible: false,
    togglePopover: jest.fn(),
    closePopover: jest.fn(),
  };
  render(
    <AdhocFilterPopoverTrigger {...controlledProps}>
      Click
    </AdhocFilterPopoverTrigger>,
  );
  expect(screen.queryByRole('tooltip')).not.toBeInTheDocument();
});
