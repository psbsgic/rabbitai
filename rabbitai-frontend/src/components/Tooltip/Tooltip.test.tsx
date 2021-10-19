import React from 'react';
import { render, screen } from 'spec/helpers/testing-library';
import userEvent from '@testing-library/user-event';
import { supersetTheme } from '@superset-ui/core';
import Button from 'src/components/Button';
import Icons from 'src/components/Icons';
import { Tooltip } from '.';

test('starts hidden with default props', () => {
  render(
    <Tooltip title="Simple tooltip">
      <Button>Hover me</Button>
    </Tooltip>,
  );
  expect(screen.queryByRole('tooltip')).not.toBeInTheDocument();
});

test('renders on hover', async () => {
  render(
    <Tooltip title="Simple tooltip">
      <Button>Hover me</Button>
    </Tooltip>,
  );
  userEvent.hover(screen.getByRole('button'));
  expect(await screen.findByRole('tooltip')).toBeInTheDocument();
});

test('renders with theme', () => {
  render(
    <Tooltip title="Simple tooltip" defaultVisible>
      <Button>Hover me</Button>
    </Tooltip>,
  );
  const tooltip = screen.getByRole('tooltip');
  expect(tooltip).toHaveStyle({
    background: `${supersetTheme.colors.grayscale.dark2}e6`,
  });
  expect(tooltip.parentNode?.parentNode).toHaveStyle({
    lineHeight: 1.6,
    fontSize: 12,
  });
});

test('renders with icon child', async () => {
  render(
    <Tooltip title="Simple tooltip">
      <Icons.Alert>Hover me</Icons.Alert>
    </Tooltip>,
  );
  userEvent.hover(screen.getByRole('img'));
  expect(await screen.findByRole('tooltip')).toBeInTheDocument();
});
