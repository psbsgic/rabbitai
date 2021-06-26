
import React from 'react';
import { render, screen } from 'spec/helpers/testing-library';
import Badge from '.';

const mockedProps = {
  count: 9,
  text: 'Text',
  textColor: 'orange',
};

test('should render', () => {
  const { container } = render(<Badge {...mockedProps} />);
  expect(container).toBeInTheDocument();
});

test('should render the count', () => {
  render(<Badge {...mockedProps} />);
  expect(screen.getAllByText('9')[0]).toBeInTheDocument();
});

test('should render the text', () => {
  render(<Badge {...mockedProps} />);
  expect(screen.getByText('Text')).toBeInTheDocument();
});

test('should render with the chosen textColor', () => {
  render(<Badge {...mockedProps} />);
  const badge = screen.getAllByText('9')[0];
  expect(badge).toHaveStyle(`
    color: 'orange';
  `);
});
