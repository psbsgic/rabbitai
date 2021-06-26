import React from 'react';
import { render, screen } from 'spec/helpers/testing-library';
import userEvent from '@testing-library/user-event';
import fetchMock from 'fetch-mock';
import RabbitaiResourceSelect from '.';

const mockedProps = {
  resource: 'dataset',
  searchColumn: 'table_name',
  onError: () => {},
};

fetchMock.get('glob:*/api/v1/dataset/?q=*', {});

test('should render', () => {
  const { container } = render(<RabbitaiResourceSelect {...mockedProps} />);
  expect(container).toBeInTheDocument();
});

test('should render the Select... placeholder', () => {
  render(<RabbitaiResourceSelect {...mockedProps} />);
  expect(screen.getByText('Select...')).toBeInTheDocument();
});

test('should render the Loading... message', () => {
  render(<RabbitaiResourceSelect {...mockedProps} />);
  const select = screen.getByText('Select...');
  userEvent.click(select);
  expect(screen.getByText('Loading...')).toBeInTheDocument();
});

test('should render the No options message', async () => {
  render(<RabbitaiResourceSelect {...mockedProps} />);
  const select = screen.getByText('Select...');
  userEvent.click(select);
  expect(await screen.findByText('No options')).toBeInTheDocument();
});

test('should render the typed text', async () => {
  render(<RabbitaiResourceSelect {...mockedProps} />);
  const select = screen.getByText('Select...');
  userEvent.click(select);
  userEvent.type(select, 'typed text');
  expect(await screen.findByText('typed text')).toBeInTheDocument();
});
