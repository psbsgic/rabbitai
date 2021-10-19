import React from 'react';
import getErrorMessageComponentRegistry from 'src/components/ErrorMessage/getErrorMessageComponentRegistry';
import { ErrorMessageComponentProps } from 'src/components/ErrorMessage/types';

// eslint-disable-next-line @typescript-eslint/no-unused-vars
const ERROR_MESSAGE_COMPONENT = (_: ErrorMessageComponentProps) => (
  <div>Test error</div>
);

// eslint-disable-next-line @typescript-eslint/no-unused-vars
const OVERRIDE_ERROR_MESSAGE_COMPONENT = (_: ErrorMessageComponentProps) => (
  <div>Custom error</div>
);

test('should return undefined for a non existent key', () => {
  expect(getErrorMessageComponentRegistry().get('INVALID_KEY')).toEqual(
    undefined,
  );
});

test('should return a component for a set key', () => {
  getErrorMessageComponentRegistry().registerValue(
    'VALID_KEY',
    ERROR_MESSAGE_COMPONENT,
  );

  expect(getErrorMessageComponentRegistry().get('VALID_KEY')).toEqual(
    ERROR_MESSAGE_COMPONENT,
  );
});

test('should return the correct component for an overridden key', () => {
  getErrorMessageComponentRegistry().registerValue(
    'OVERRIDE_KEY',
    ERROR_MESSAGE_COMPONENT,
  );

  getErrorMessageComponentRegistry().registerValue(
    'OVERRIDE_KEY',
    OVERRIDE_ERROR_MESSAGE_COMPONENT,
  );

  expect(getErrorMessageComponentRegistry().get('OVERRIDE_KEY')).toEqual(
    OVERRIDE_ERROR_MESSAGE_COMPONENT,
  );
});
