
import getEffectiveExtraFilters from 'src/dashboard/util/charts/getEffectiveExtraFilters';

describe('getEffectiveExtraFilters', () => {
  it('should create valid filters', () => {
    const result = getEffectiveExtraFilters({
      gender: ['girl'],
      name: null,
      __time_range: ' : 2020-07-17T00:00:00',
    });
    expect(result).toMatchObject([
      {
        col: 'gender',
        op: 'IN',
        val: ['girl'],
      },
      {
        col: '__time_range',
        op: '==',
        val: ' : 2020-07-17T00:00:00',
      },
    ]);
  });
});
