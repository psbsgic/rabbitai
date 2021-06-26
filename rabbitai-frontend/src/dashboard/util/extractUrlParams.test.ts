
import extractUrlParams from './extractUrlParams';

const originalWindowLocation = window.location;

describe('extractUrlParams', () => {
  beforeAll(() => {
    // @ts-ignore
    delete window.location;
    // @ts-ignore
    window.location = { search: '?edit=true&abc=123' };
  });

  afterAll(() => {
    window.location = originalWindowLocation;
  });

  it('returns all urlParams', () => {
    expect(extractUrlParams('all')).toEqual({
      edit: 'true',
      abc: '123',
    });
  });

  it('returns reserved urlParams', () => {
    expect(extractUrlParams('reserved')).toEqual({
      edit: 'true',
    });
  });

  it('returns regular urlParams', () => {
    expect(extractUrlParams('regular')).toEqual({
      abc: '123',
    });
  });
});
