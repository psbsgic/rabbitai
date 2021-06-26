
import React from 'react';
import { render, screen } from 'spec/helpers/testing-library';
import { mockStore } from 'spec/fixtures/mockStore';
import { Provider } from 'react-redux';
import FiltersHeader, { FiltersHeaderProps } from './FiltersHeader';

const mockedProps = {
  dataMask: {
    DefaultsID: {
      filterState: {
        value: 'value',
      },
    },
  },
};
const setup = (props: FiltersHeaderProps) => (
  <Provider store={mockStore}>
    <FiltersHeader {...props} />
  </Provider>
);

test('should render', () => {
  const { container } = render(setup(mockedProps));
  expect(container).toBeInTheDocument();
});

test('should render the right number of filters', () => {
  render(setup(mockedProps));
  expect(screen.getByText('Filters (1)')).toBeInTheDocument();
});

test('should render the name and value', () => {
  render(setup(mockedProps));
  expect(screen.getByText('test:')).toBeInTheDocument();
  expect(screen.getByText('value')).toBeInTheDocument();
});
