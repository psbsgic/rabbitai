import React from 'react';
import { render, screen } from 'spec/helpers/testing-library';
import userEvent from '@testing-library/user-event';
import FilterConfigurationLink from '.';

test('should render', () => {
  const { container } = render(
    <FilterConfigurationLink>Config link</FilterConfigurationLink>,
    {
      useRedux: true,
    },
  );
  expect(container).toBeInTheDocument();
});

test('should render the config link text', () => {
  render(<FilterConfigurationLink>Config link</FilterConfigurationLink>, {
    useRedux: true,
  });
  expect(screen.getByText('Config link')).toBeInTheDocument();
});

test('should render the modal on click', () => {
  render(<FilterConfigurationLink>Config link</FilterConfigurationLink>, {
    useRedux: true,
  });
  const configLink = screen.getByText('Config link');
  expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
  userEvent.click(configLink);
  expect(screen.getByRole('dialog')).toBeInTheDocument();
});
