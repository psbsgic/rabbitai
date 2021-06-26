import { testWithId } from './testUtils';

describe('testUtils', () => {
  it('testWithId with prefix only', () => {
    expect(testWithId('prefix')()).toEqual({ 'data-test': 'prefix' });
  });

  it('testWithId with prefix only and idOnly', () => {
    expect(testWithId('prefix', true)()).toEqual('prefix');
  });

  it('testWithId with id only', () => {
    expect(testWithId()('id')).toEqual({ 'data-test': 'id' });
  });

  it('testWithId with id only and idOnly', () => {
    expect(testWithId(undefined, true)('id')).toEqual('id');
  });

  it('testWithId with prefix and id', () => {
    expect(testWithId('prefix')('id')).toEqual({ 'data-test': 'prefix__id' });
  });

  it('testWithId with prefix and id and idOnly', () => {
    expect(testWithId('prefix', true)('id')).toEqual('prefix__id');
  });

  it('testWithId without prefix and id', () => {
    expect(testWithId()()).toEqual({ 'data-test': '' });
  });

  it('testWithId without prefix and id and idOnly', () => {
    expect(testWithId(undefined, true)()).toEqual('');
  });
});
