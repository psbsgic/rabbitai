
import React from 'react';
import { render, screen } from 'spec/helpers/testing-library';
import userEvent from '@testing-library/user-event';
import fetchMock from 'fetch-mock';
import URLShortLinkButton from 'src/components/URLShortLinkButton';
import ToastPresenter from 'src/messageToasts/containers/ToastPresenter';

const fakeUrl = 'http://fakeurl.com';

fetchMock.post('glob:*/r/shortner/', fakeUrl);

test('renders with default props', () => {
  render(<URLShortLinkButton />, { useRedux: true });
  expect(screen.getByRole('button')).toBeInTheDocument();
});

test('renders overlay on click', async () => {
  render(<URLShortLinkButton />, { useRedux: true });
  userEvent.click(screen.getByRole('button'));
  expect(await screen.findByRole('tooltip')).toBeInTheDocument();
});

test('obtains short url', async () => {
  render(<URLShortLinkButton />, { useRedux: true });
  userEvent.click(screen.getByRole('button'));
  expect(await screen.findByRole('tooltip')).toHaveTextContent(fakeUrl);
});

test('creates email anchor', async () => {
  const subject = 'Subject';
  const content = 'Content';

  render(<URLShortLinkButton emailSubject={subject} emailContent={content} />, {
    useRedux: true,
  });

  const href = `mailto:?Subject=${subject}%20&Body=${content}${fakeUrl}`;
  userEvent.click(screen.getByRole('button'));
  expect(await screen.findByRole('link')).toHaveAttribute('href', href);
});

test('renders error message on short url error', async () => {
  fetchMock.mock('glob:*/r/shortner/', 500, {
    overwriteRoutes: true,
  });

  render(
    <>
      <URLShortLinkButton />
      <ToastPresenter />
    </>,
    { useRedux: true },
  );
  userEvent.click(screen.getByRole('button'));
  expect(await screen.findByRole('alert')).toBeInTheDocument();
});
