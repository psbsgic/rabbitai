
import { generateFiltersSetId } from '.';

test('Should follow the pattern "FILTERS_SET-"', () => {
  const id = generateFiltersSetId();
  expect(id.startsWith('FILTERS_SET-', 0)).toBe(true);
});
