import React from 'react';
import { render, screen, waitFor } from 'spec/helpers/testing-library';
import userEvent from '@testing-library/user-event';
import CopyToClipboard from '.';

test('renders with default props', () => {
  const text = 'Text';
  render(<CopyToClipboard text={text} />, { useRedux: true });
  expect(screen.getByText(text)).toBeInTheDocument();
  expect(screen.getByText('Copy')).toBeInTheDocument();
});

test('renders with custom copy node', () => {
  const copyNode = <a href="/">Custom node</a>;
  render(<CopyToClipboard copyNode={copyNode} />, { useRedux: true });
  expect(screen.getByRole('link')).toBeInTheDocument();
});

test('renders without text showing', () => {
  const text = 'Text';
  render(<CopyToClipboard text={text} shouldShowText={false} />, {
    useRedux: true,
  });
  expect(screen.queryByText(text)).not.toBeInTheDocument();
});

test('getText on copy', async () => {
  const getText = jest.fn(() => 'Text');
  render(<CopyToClipboard getText={getText} />, { useRedux: true });
  userEvent.click(screen.getByText('Copy'));
  await waitFor(() => expect(getText).toHaveBeenCalled());
});

test('renders tooltip on hover', async () => {
  const tooltipText = 'Tooltip';
  render(<CopyToClipboard tooltipText={tooltipText} />, { useRedux: true });
  userEvent.hover(screen.getByText('Copy'));
  const tooltip = await screen.findByRole('tooltip');
  expect(tooltip).toBeInTheDocument();
  expect(tooltip).toHaveTextContent(tooltipText);
});

test('triggers onCopyEnd', async () => {
  const onCopyEnd = jest.fn();
  render(<CopyToClipboard onCopyEnd={onCopyEnd} />, {
    useRedux: true,
  });
  userEvent.click(screen.getByText('Copy'));
  await waitFor(() => expect(onCopyEnd).toHaveBeenCalled());
});

test('renders unwrapped', () => {
  const text = 'Text';
  render(<CopyToClipboard text={text} wrapped={false} />, {
    useRedux: true,
  });
  expect(screen.queryByText(text)).not.toBeInTheDocument();
});
