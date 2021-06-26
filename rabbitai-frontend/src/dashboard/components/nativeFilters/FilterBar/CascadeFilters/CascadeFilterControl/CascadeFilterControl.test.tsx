
import React from 'react';
import { render, screen } from 'spec/helpers/testing-library';
import { mockStore } from 'spec/fixtures/mockStore';
import { Provider } from 'react-redux';
import { nativeFiltersInfo } from 'spec/javascripts/dashboard/fixtures/mockNativeFilters';
import CascadeFilterControl, { CascadeFilterControlProps } from '.';

const mockedProps = {
  filter: {
    ...nativeFiltersInfo.filters.DefaultsID,
    cascadeChildren: [
      {
        ...nativeFiltersInfo.filters.DefaultsID,
        name: 'test child filter 1',
        cascadeChildren: [],
      },
      {
        ...nativeFiltersInfo.filters.DefaultsID,
        name: 'test child filter 2',
        cascadeChildren: [
          {
            ...nativeFiltersInfo.filters.DefaultsID,
            name: 'test child of a child filter',
            cascadeChildren: [],
          },
        ],
      },
    ],
  },
  onFilterSelectionChange: jest.fn(),
};

const setup = (props: CascadeFilterControlProps) => (
  <Provider store={mockStore}>
    <CascadeFilterControl {...props} />
  </Provider>
);

test('should render', () => {
  const { container } = render(setup(mockedProps));
  expect(container).toBeInTheDocument();
});

test('should render the filter name', () => {
  render(setup(mockedProps));
  expect(screen.getByText('test')).toBeInTheDocument();
});

test('should render the children filter names', () => {
  render(setup(mockedProps));
  expect(screen.getByText('test child filter 1')).toBeInTheDocument();
  expect(screen.getByText('test child filter 2')).toBeInTheDocument();
});

test('should render the child of a child filter name', () => {
  render(setup(mockedProps));
  expect(screen.getByText('test child of a child filter')).toBeInTheDocument();
});
