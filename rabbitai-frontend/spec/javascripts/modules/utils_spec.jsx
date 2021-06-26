
import { mainMetric } from 'src/modules/utils';

describe('utils', () => {
  describe('mainMetric', () => {
    it('is null when no options', () => {
      expect(mainMetric([])).toBeUndefined();
      expect(mainMetric(null)).toBeUndefined();
    });
    it('prefers the "count" metric when first', () => {
      const metrics = [{ metric_name: 'count' }, { metric_name: 'foo' }];
      expect(mainMetric(metrics)).toBe('count');
    });
    it('prefers the "count" metric when not first', () => {
      const metrics = [{ metric_name: 'foo' }, { metric_name: 'count' }];
      expect(mainMetric(metrics)).toBe('count');
    });
    it('selects the first metric when "count" is not an option', () => {
      const metrics = [{ metric_name: 'foo' }, { metric_name: 'not_count' }];
      expect(mainMetric(metrics)).toBe('foo');
    });
  });
});
