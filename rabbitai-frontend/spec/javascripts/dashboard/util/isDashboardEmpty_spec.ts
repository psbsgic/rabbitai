import isDashboardEmpty from 'src/dashboard/util/isDashboardEmpty';
import getEmptyLayout from 'src/dashboard/util/getEmptyLayout';

describe('isDashboardEmpty', () => {
  const emptyLayout: object = getEmptyLayout();
  const testLayout: object = {
    ...emptyLayout,
    'MARKDOWN-IhTGLhyiTd': {
      children: [],
      id: 'MARKDOWN-IhTGLhyiTd',
      meta: { code: 'test me', height: 50, width: 4 },
      parents: ['ROOT_ID', 'GRID_ID', 'ROW-uPjcKNYJQy'],
      type: 'MARKDOWN',
    },
  };

  it('should return true for empty dashboard', () => {
    expect(isDashboardEmpty(emptyLayout)).toBe(true);
  });

  it('should return false for non-empty dashboard', () => {
    expect(isDashboardEmpty(testLayout)).toBe(false);
  });
});
