
import userEvent from '@testing-library/user-event';
import React from 'react';
import { render, screen } from 'spec/helpers/testing-library';
import { CopyToClipboardButton } from '.';

test('Render a button', () => {
  render(<CopyToClipboardButton data={{ copy: 'data', data: 'copy' }} />, {
    useRedux: true,
  });
  expect(screen.getByRole('button')).toBeInTheDocument();
});

test('Should copy to clipboard', () => {
  document.execCommand = jest.fn();

  render(<CopyToClipboardButton data={{ copy: 'data', data: 'copy' }} />, {
    useRedux: true,
  });

  expect(document.execCommand).toHaveBeenCalledTimes(0);
  userEvent.click(screen.getByRole('button'));
  expect(document.execCommand).toHaveBeenCalledWith('copy');
});
