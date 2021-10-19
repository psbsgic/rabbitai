import { getFilterValueForDisplay } from '.';

test('Should return "" when value is null or undefined', () => {
  expect(getFilterValueForDisplay(null)).toBe('');
  expect(getFilterValueForDisplay(undefined)).toBe('');
  expect(getFilterValueForDisplay()).toBe('');
});

test('Should return "string value" when value is string or number', () => {
  expect(getFilterValueForDisplay(123)).toBe('123');
  expect(getFilterValueForDisplay('123')).toBe('123');
});

test('Should return a string with values ​​separated by commas', () => {
  expect(getFilterValueForDisplay(['a', 'b', 'c'])).toBe('a, b, c');
});

test('Should return a JSON.stringify from objects', () => {
  expect(getFilterValueForDisplay({ any: 'value' })).toBe('{"any":"value"}');
});

test('Should return an error message when the type is invalid', () => {
  expect(getFilterValueForDisplay(true as any)).toBe('Unknown value');
});
