

import { setCrossFilterFieldValues } from '.';

test('setValues', () => {
  const from = { setFieldsValue: jest.fn() };
  const values = {
    val01: 'val01',
    val02: 'val02',
    val03: 'val03',
    val04: 'val04',
  };
  setCrossFilterFieldValues(from as any, values);

  expect(from.setFieldsValue).toBeCalledTimes(1);
  expect(from.setFieldsValue).toBeCalledWith(values);
});
