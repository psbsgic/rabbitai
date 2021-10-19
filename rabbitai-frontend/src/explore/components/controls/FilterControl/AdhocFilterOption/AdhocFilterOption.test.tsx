import React from 'react';
import { render, screen, waitFor } from 'spec/helpers/testing-library';
import userEvent from '@testing-library/user-event';
import { HTML5Backend } from 'react-dnd-html5-backend';
import { DndProvider } from 'react-dnd';
import AdhocFilter, {
  EXPRESSION_TYPES,
  CLAUSES,
} from 'src/explore/components/controls/FilterControl/AdhocFilter';
import AdhocFilterOption from '.';

const simpleAdhocFilter = new AdhocFilter({
  expressionType: EXPRESSION_TYPES.SIMPLE,
  subject: 'value',
  operator: '>',
  comparator: '10',
  clause: CLAUSES.WHERE,
});

const options = [
  { type: 'VARCHAR(255)', column_name: 'source', id: 1 },
  { type: 'VARCHAR(255)', column_name: 'target', id: 2 },
  { type: 'DOUBLE', column_name: 'value', id: 3 },
];

const mockedProps = {
  adhocFilter: simpleAdhocFilter,
  onFilterEdit: jest.fn(),
  options,
};

const setup = (props: {
  adhocFilter: typeof simpleAdhocFilter;
  onFilterEdit: () => void;
  options: {
    type: string;
    column_name: string;
    id: number;
  }[];
}) => (
  <DndProvider backend={HTML5Backend}>
    <AdhocFilterOption {...props} />
  </DndProvider>
);

test('should render', async () => {
  const { container } = render(setup(mockedProps));
  await waitFor(() => expect(container).toBeInTheDocument());
});

test('should render the control label', async () => {
  render(setup(mockedProps));
  expect(await screen.findByText('value > 10')).toBeInTheDocument();
});

test('should render the remove button', async () => {
  render(setup(mockedProps));
  const removeBtn = await screen.findByRole('button');
  expect(removeBtn).toBeInTheDocument();
});

test('should render the right caret', async () => {
  render(setup(mockedProps));
  expect(
    await screen.findByRole('img', { name: 'caret-right' }),
  ).toBeInTheDocument();
});

test('should render the Popover on clicking the right caret', async () => {
  render(setup(mockedProps));
  const rightCaret = await screen.findByRole('img', { name: 'caret-right' });
  userEvent.click(rightCaret);
  expect(screen.getByRole('tooltip')).toBeInTheDocument();
});
