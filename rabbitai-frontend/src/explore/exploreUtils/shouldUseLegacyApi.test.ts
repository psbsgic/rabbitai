import * as Core from '@superset-ui/core';
import { shouldUseLegacyApi } from '.';

test('Should return false', () => {
  const spy = jest.spyOn(Core, 'getChartMetadataRegistry');
  const get = jest.fn();
  spy.mockReturnValue({ get } as any);
  expect(get).toBeCalledTimes(0);
  expect(shouldUseLegacyApi({ viz_type: 'name_test' })).toBe(false);
  expect(get).toBeCalledTimes(1);
  expect(get).toBeCalledWith('name_test');
});

test('Should return true', () => {
  const spy = jest.spyOn(Core, 'getChartMetadataRegistry');
  const get = jest.fn();
  get.mockReturnValue({ useLegacyApi: true });
  spy.mockReturnValue({ get } as any);
  expect(get).toBeCalledTimes(0);
  expect(shouldUseLegacyApi({ viz_type: 'name_test' })).toBe(true);
  expect(get).toBeCalledTimes(1);
  expect(get).toBeCalledWith('name_test');
});

test('Should return false when useLegacyApi:false', () => {
  const spy = jest.spyOn(Core, 'getChartMetadataRegistry');
  const get = jest.fn();
  get.mockReturnValue({ useLegacyApi: false });
  spy.mockReturnValue({ get } as any);
  expect(get).toBeCalledTimes(0);
  expect(shouldUseLegacyApi({ viz_type: 'name_test' })).toBe(false);
  expect(get).toBeCalledTimes(1);
  expect(get).toBeCalledWith('name_test');
});
