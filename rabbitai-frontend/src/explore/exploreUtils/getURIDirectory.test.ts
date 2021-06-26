
import { getURIDirectory } from '.';

test('Cases in which the "explore_json" will be returned', () => {
  ['full', 'json', 'csv', 'query', 'results', 'samples'].forEach(name => {
    expect(getURIDirectory(name)).toBe('/rabbitai/explore_json/');
  });
});

test('Cases in which the "explore" will be returned', () => {
  expect(getURIDirectory('any-string')).toBe('/rabbitai/explore/');
  expect(getURIDirectory()).toBe('/rabbitai/explore/');
});
