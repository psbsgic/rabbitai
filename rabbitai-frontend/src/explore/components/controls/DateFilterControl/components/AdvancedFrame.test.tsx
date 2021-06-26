
import React from 'react';
import { render, screen } from 'spec/helpers/testing-library';
import userEvent from '@testing-library/user-event';
import { AdvancedFrame } from '.';

test('renders with default props', () => {
  render(<AdvancedFrame onChange={jest.fn()} value="Last week" />);
  expect(screen.getByText('Configure Advanced Time Range')).toBeInTheDocument();
});

test('render with empty value', () => {
  render(<AdvancedFrame onChange={jest.fn()} value="" />);
  expect(screen.getByText('Configure Advanced Time Range')).toBeInTheDocument();
});

test('triggers since onChange', () => {
  const onChange = jest.fn();
  render(<AdvancedFrame onChange={onChange} value="Next week" />);
  userEvent.type(screen.getAllByRole('textbox')[0], 'Last week');
  expect(onChange).toHaveBeenCalled();
});

test('triggers until onChange', () => {
  const onChange = jest.fn();
  render(<AdvancedFrame onChange={onChange} value="today : tomorrow" />);
  userEvent.type(screen.getAllByRole('textbox')[1], 'dayAfterTomorrow');
  expect(onChange).toHaveBeenCalled();
});
