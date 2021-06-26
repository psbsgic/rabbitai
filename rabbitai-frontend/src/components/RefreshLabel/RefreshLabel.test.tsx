
import React from 'react';
import { render, screen } from 'spec/helpers/testing-library';
import userEvent from '@testing-library/user-event';
import RefreshLabel from 'src/components/RefreshLabel';

test('renders with default props', () => {
  render(<RefreshLabel tooltipContent="Tooltip" onClick={jest.fn()} />);
  const refresh = screen.getByRole('button');
  expect(refresh).toBeInTheDocument();
  userEvent.hover(refresh);
});

test('renders tooltip on hover', async () => {
  const tooltipText = 'Tooltip';
  render(<RefreshLabel tooltipContent={tooltipText} onClick={jest.fn()} />);
  const refresh = screen.getByRole('button');
  userEvent.hover(refresh);
  const tooltip = await screen.findByRole('tooltip');
  expect(tooltip).toBeInTheDocument();
  expect(tooltip).toHaveTextContent(tooltipText);
});

test('triggers on click event', () => {
  const onClick = jest.fn();
  render(<RefreshLabel tooltipContent="Tooltip" onClick={onClick} />);
  const refresh = screen.getByRole('button');
  userEvent.click(refresh);
  expect(onClick).toHaveBeenCalled();
});
