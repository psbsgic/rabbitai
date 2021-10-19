import React from 'react';
import { render, screen } from 'spec/helpers/testing-library';
import { mockStore } from 'spec/fixtures/mockStore';
import { Provider } from 'react-redux';
import FilterSets, { FilterSetsProps } from '.';

const createProps = () => ({
  disabled: false,
  isFilterSetChanged: false,
  dataMaskSelected: {
    DefaultsID: {
      filterState: {
        value: 'value',
      },
    },
  },
  onEditFilterSet: jest.fn(),
  onFilterSelectionChange: jest.fn(),
});

const setup = (props: FilterSetsProps) => (
  <Provider store={mockStore}>
    <FilterSets {...props} />
  </Provider>
);

test('should render', () => {
  const mockedProps = createProps();
  const { container } = render(setup(mockedProps));
  expect(container).toBeInTheDocument();
});

test('should render the default title', () => {
  const mockedProps = createProps();
  render(setup(mockedProps));
  expect(screen.getByText('New filter set')).toBeInTheDocument();
});

test('should render the right number of filters', () => {
  const mockedProps = createProps();
  render(setup(mockedProps));
  expect(screen.getByText('Filters (1)')).toBeInTheDocument();
});

test('should render the filters', () => {
  const mockedProps = createProps();
  render(setup(mockedProps));
  expect(screen.getByText('Set name')).toBeInTheDocument();
});
