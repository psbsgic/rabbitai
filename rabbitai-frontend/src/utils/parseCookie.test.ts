import parseCookie from 'src/utils/parseCookie';

describe('parseCookie', () => {
  let cookieVal = '';
  Object.defineProperty(document, 'cookie', {
    get: jest.fn().mockImplementation(() => cookieVal),
  });
  it('parses cookie strings', () => {
    cookieVal = 'val1=foo; val2=bar';
    expect(parseCookie()).toEqual({ val1: 'foo', val2: 'bar' });
  });

  it('parses empty cookie strings', () => {
    cookieVal = '';
    expect(parseCookie()).toEqual({});
  });

  it('accepts an arg', () => {
    expect(parseCookie('val=foo')).toEqual({ val: 'foo' });
  });
});
