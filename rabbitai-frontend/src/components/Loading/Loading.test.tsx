

import React from 'react';
import '@testing-library/jest-dom';
import { render, screen } from '@testing-library/react';
import Loading from './index';

test('Rerendering correctly with default props', () => {
  render(<Loading />);
  const loading = screen.getByRole('status');
  const classNames = loading.getAttribute('class')?.split(' ');
  const imagePath = loading.getAttribute('src');
  const ariaLive = loading.getAttribute('aria-live');
  const ariaLabel = loading.getAttribute('aria-label');
  expect(loading).toBeInTheDocument();
  expect(imagePath).toBe('/static/assets/images/loading.gif');
  expect(classNames).toContain('floating');
  expect(classNames).toContain('loading');
  expect(ariaLive).toContain('polite');
  expect(ariaLabel).toContain('Loading');
});

test('Position must be a class', () => {
  render(<Loading position="normal" />);
  const loading = screen.getByRole('status');
  const classNames = loading.getAttribute('class')?.split(' ');
  expect(loading).toBeInTheDocument();
  expect(classNames).not.toContain('floating');
  expect(classNames).toContain('normal');
});

test('support for extra classes', () => {
  render(<Loading className="extra-class" />);
  const loading = screen.getByRole('status');
  const classNames = loading.getAttribute('class')?.split(' ');
  expect(loading).toBeInTheDocument();
  expect(classNames).toContain('loading');
  expect(classNames).toContain('floating');
  expect(classNames).toContain('extra-class');
});

test('Diferent image path', () => {
  render(<Loading image="/images/loading.gif" />);
  const loading = screen.getByRole('status');
  const imagePath = loading.getAttribute('src');
  expect(loading).toBeInTheDocument();
  expect(imagePath).toBe('/images/loading.gif');
});
