
import { getNestedValue, interpolate } from 'src/showSavedQuery/utils';

describe('getNestedValue', () => {
  it('is a function', () => {
    expect(typeof getNestedValue).toBe('function');
  });

  it('works with simple ids', () => {
    const obj = { a: '1' };
    const id = 'a';
    expect(getNestedValue(obj, id)).toEqual('1');
  });

  it('works with complex ids', () => {
    const obj = { a: { b: '1' } };
    const id = 'a.b';
    expect(getNestedValue(obj, id)).toEqual('1');
  });

  it('works with other separators', () => {
    const obj = { a: { b: { c: '1' } } };
    const id = 'a__b__c';
    const separator = '__';
    expect(getNestedValue(obj, id, separator)).toEqual('1');
  });
});

describe('interpolate', () => {
  it('is a function', () => {
    expect(typeof interpolate).toBe('function');
  });

  it('works with simple ids', () => {
    const obj = { a: '1' };
    // eslint-disable-next-line no-template-curly-in-string
    const str = 'value: ${a}';
    expect(interpolate(str, obj)).toEqual('value: 1');
  });

  it('works with complex ids', () => {
    const obj = { a: { b: '1' } };
    // eslint-disable-next-line no-template-curly-in-string
    const str = 'value: ${a.b}';
    expect(interpolate(str, obj)).toEqual('value: 1');
  });
});
