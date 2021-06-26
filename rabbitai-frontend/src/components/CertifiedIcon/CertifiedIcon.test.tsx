
import React from 'react';
import { render, screen } from 'spec/helpers/testing-library';
import userEvent from '@testing-library/user-event';
import CertifiedIcon from 'src/components/CertifiedIcon';

test('renders with default props', () => {
  render(<CertifiedIcon />);
  expect(screen.getByRole('img')).toBeInTheDocument();
});

test('renders a tooltip when hovered', async () => {
  render(<CertifiedIcon />);
  userEvent.hover(screen.getByRole('img'));
  expect(await screen.findByRole('tooltip')).toBeInTheDocument();
});

test('renders with certified by', async () => {
  const certifiedBy = 'Trusted Authority';
  render(<CertifiedIcon certifiedBy={certifiedBy} />);
  userEvent.hover(screen.getByRole('img'));
  expect(await screen.findByRole('tooltip')).toHaveTextContent(certifiedBy);
});

test('renders with details', async () => {
  const details = 'All requirements have been met.';
  render(<CertifiedIcon details={details} />);
  userEvent.hover(screen.getByRole('img'));
  expect(await screen.findByRole('tooltip')).toHaveTextContent(details);
});
