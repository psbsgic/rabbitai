
import React from 'react';
import { render, screen, waitFor } from 'spec/helpers/testing-library';
import userEvent from '@testing-library/user-event';
import Alert, { AlertProps } from 'src/components/Alert';

type AlertType = Pick<AlertProps, 'type'>;
type AlertTypeValue = AlertType[keyof AlertType];

test('renders with default props', async () => {
  render(<Alert message="Message" />);

  expect(screen.getByRole('alert')).toHaveTextContent('Message');
  expect(await screen.findByLabelText(`info icon`)).toBeInTheDocument();
  expect(await screen.findByLabelText('close icon')).toBeInTheDocument();
});

test('renders each type', async () => {
  const types: AlertTypeValue[] = ['info', 'error', 'warning', 'success'];
  for (let i = 0; i < types.length; i += 1) {
    const type = types[i];
    render(<Alert type={type} message="Message" />);
    // eslint-disable-next-line no-await-in-loop
    expect(await screen.findByLabelText(`${type} icon`)).toBeInTheDocument();
  }
});

test('renders without close button', async () => {
  render(<Alert message="Message" closable={false} />);

  await waitFor(() => {
    expect(screen.queryByLabelText('close icon')).not.toBeInTheDocument();
  });
});

test('disappear when closed', () => {
  render(<Alert message="Message" />);
  userEvent.click(screen.queryByLabelText('close icon')!);
  expect(screen.queryByRole('alert')).not.toBeInTheDocument();
});

test('renders without icon', async () => {
  const type = 'info';
  render(<Alert type={type} message="Message" showIcon={false} />);
  await waitFor(() => {
    expect(screen.queryByLabelText(`${type} icon`)).not.toBeInTheDocument();
  });
});

test('renders message', () => {
  render(<Alert message="Message" />);
  expect(screen.getByRole('alert')).toHaveTextContent('Message');
});

test('renders message and description', () => {
  render(<Alert message="Message" description="Description" />);
  expect(screen.getByRole('alert')).toHaveTextContent('Message');
  expect(screen.getByRole('alert')).toHaveTextContent('Description');
});
