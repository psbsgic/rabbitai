import 'jest-enzyme';
import './shim';
import { configure as configureTestingLibrary } from '@testing-library/react';

configureTestingLibrary({
  testIdAttribute: 'data-test',
});
