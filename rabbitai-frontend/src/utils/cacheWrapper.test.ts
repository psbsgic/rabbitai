import { cacheWrapper } from 'src/utils/cacheWrapper';

describe('cacheWrapper', () => {
  const fnResult = 'fnResult';
  const fn = jest.fn<string, [number, number]>().mockReturnValue(fnResult);

  let wrappedFn: (a: number, b: number) => string;

  beforeEach(() => {
    const cache = new Map<string, any>();
    wrappedFn = cacheWrapper(fn, cache);
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('calls fn with its arguments once when the key is not found', () => {
    const returnedValue = wrappedFn(1, 2);

    expect(returnedValue).toEqual(fnResult);
    expect(fn).toBeCalledTimes(1);
    expect(fn).toBeCalledWith(1, 2);
  });

  describe('subsequent calls', () => {
    it('returns the correct value without fn being called multiple times', () => {
      const returnedValue1 = wrappedFn(1, 2);
      const returnedValue2 = wrappedFn(1, 2);

      expect(returnedValue1).toEqual(fnResult);
      expect(returnedValue2).toEqual(fnResult);
      expect(fn).toBeCalledTimes(1);
    });

    it('fn is called multiple times for different arguments', () => {
      wrappedFn(1, 2);
      wrappedFn(1, 3);

      expect(fn).toBeCalledTimes(2);
    });
  });

  describe('with custom keyFn', () => {
    let cache: Map<string, any>;

    beforeEach(() => {
      cache = new Map<string, any>();
      wrappedFn = cacheWrapper(fn, cache, (...args) => `key-${args[0]}`);
    });

    it('saves fn result in cache under generated key', () => {
      wrappedFn(1, 2);
      expect(cache.get('key-1')).toEqual(fnResult);
    });

    it('subsequent calls with same generated key calls fn once, even if other arguments have changed', () => {
      wrappedFn(1, 1);
      wrappedFn(1, 2);
      wrappedFn(1, 3);

      expect(fn).toBeCalledTimes(1);
    });
  });
});
