import React from 'react';
import { render, screen, fireEvent } from 'spec/helpers/testing-library';
import { isFeatureEnabled } from 'src/featureFlags';
import OmniContainer from './index';

jest.mock('src/featureFlags', () => ({
  isFeatureEnabled: jest.fn(),
  FeatureFlag: { OMNIBAR: 'OMNIBAR' },
}));

test('Do not open Omnibar with the featureflag disabled', () => {
  (isFeatureEnabled as jest.Mock).mockImplementation(
    (ff: string) => !(ff === 'OMNIBAR'),
  );
  const logEvent = jest.fn();
  render(
    <div data-test="test">
      <OmniContainer logEvent={logEvent} />
    </div>,
  );

  expect(
    screen.queryByPlaceholderText('Search all dashboards'),
  ).not.toBeInTheDocument();
  fireEvent.keyDown(screen.getByTestId('test'), {
    ctrlKey: true,
    code: 'KeyK',
  });
  expect(
    screen.queryByPlaceholderText('Search all dashboards'),
  ).not.toBeInTheDocument();
});

test('Open Omnibar with ctrl + k with featureflag enabled', () => {
  (isFeatureEnabled as jest.Mock).mockImplementation(
    (ff: string) => ff === 'OMNIBAR',
  );
  const logEvent = jest.fn();
  render(
    <div data-test="test">
      <OmniContainer logEvent={logEvent} />
    </div>,
  );

  expect(
    screen.queryByPlaceholderText('Search all dashboards'),
  ).not.toBeInTheDocument();

  // show Omnibar
  fireEvent.keyDown(screen.getByTestId('test'), {
    ctrlKey: true,
    code: 'KeyK',
  });
  expect(
    screen.queryByPlaceholderText('Search all dashboards'),
  ).toBeInTheDocument();

  // hide Omnibar
  fireEvent.keyDown(screen.getByTestId('test'), {
    ctrlKey: true,
    code: 'KeyK',
  });
  expect(
    screen.queryByPlaceholderText('Search all dashboards'),
  ).not.toBeVisible();
});

test('Open Omnibar with ctrl + s with featureflag enabled', () => {
  (isFeatureEnabled as jest.Mock).mockImplementation(
    (ff: string) => ff === 'OMNIBAR',
  );
  const logEvent = jest.fn();
  render(
    <div data-test="test">
      <OmniContainer logEvent={logEvent} />
    </div>,
  );

  expect(
    screen.queryByPlaceholderText('Search all dashboards'),
  ).not.toBeInTheDocument();

  // show Omnibar
  fireEvent.keyDown(screen.getByTestId('test'), {
    ctrlKey: true,
    code: 'KeyS',
  });
  expect(
    screen.queryByPlaceholderText('Search all dashboards'),
  ).toBeInTheDocument();

  // hide Omnibar
  fireEvent.keyDown(screen.getByTestId('test'), {
    ctrlKey: true,
    code: 'KeyS',
  });
  expect(
    screen.queryByPlaceholderText('Search all dashboards'),
  ).not.toBeVisible();
});

test('Open Omnibar with Command + k with featureflag enabled', () => {
  (isFeatureEnabled as jest.Mock).mockImplementation(
    (ff: string) => ff === 'OMNIBAR',
  );
  const logEvent = jest.fn();
  render(
    <div data-test="test">
      <OmniContainer logEvent={logEvent} />
    </div>,
  );

  expect(
    screen.queryByPlaceholderText('Search all dashboards'),
  ).not.toBeInTheDocument();

  // show Omnibar
  fireEvent.keyDown(screen.getByTestId('test'), {
    metaKey: true,
    code: 'KeyK',
  });
  expect(
    screen.queryByPlaceholderText('Search all dashboards'),
  ).toBeInTheDocument();

  // hide Omnibar
  fireEvent.keyDown(screen.getByTestId('test'), {
    metaKey: true,
    code: 'KeyK',
  });
  expect(
    screen.queryByPlaceholderText('Search all dashboards'),
  ).not.toBeVisible();
});

test('Open Omnibar with Command + s with featureflag enabled', () => {
  (isFeatureEnabled as jest.Mock).mockImplementation(
    (ff: string) => ff === 'OMNIBAR',
  );
  const logEvent = jest.fn();
  render(
    <div data-test="test">
      <OmniContainer logEvent={logEvent} />
    </div>,
  );

  expect(
    screen.queryByPlaceholderText('Search all dashboards'),
  ).not.toBeInTheDocument();

  // show Omnibar
  fireEvent.keyDown(screen.getByTestId('test'), {
    metaKey: true,
    code: 'KeyS',
  });
  expect(
    screen.queryByPlaceholderText('Search all dashboards'),
  ).toBeInTheDocument();

  // hide Omnibar
  fireEvent.keyDown(screen.getByTestId('test'), {
    metaKey: true,
    code: 'KeyS',
  });
  expect(
    screen.queryByPlaceholderText('Search all dashboards'),
  ).not.toBeVisible();
});
