import React from 'react';
import { render } from 'spec/helpers/testing-library';
import FilterScope from 'src/dashboard/components/nativeFilters/FiltersConfigModal/FiltersConfigForm/FilterScope/FilterScope';
import CrossFilterScopingForm from '.';

jest.mock(
  'src/dashboard/components/nativeFilters/FiltersConfigModal/FiltersConfigForm/FilterScope/FilterScope',
  () => jest.fn(() => null),
);

const createProps = () => {
  const getFieldValue = jest.fn();
  getFieldValue.mockImplementation(name => name);
  return {
    chartId: 123,
    scope: 'Scope',
    form: { getFieldValue },
  };
};

test('Should send correct props', () => {
  const props = createProps();
  render(<CrossFilterScopingForm {...(props as any)} />);

  expect(FilterScope).toHaveBeenCalledWith(
    expect.objectContaining({
      chartId: 123,
      filterScope: 'Scope',
      formFilterScope: 'scope',
      formScopingType: 'scoping',
    }),
    {},
  );
});

test('Should get correct filds', () => {
  const props = createProps();
  render(<CrossFilterScopingForm {...(props as any)} />);
  expect(props.form.getFieldValue).toBeCalledTimes(2);
  expect(props.form.getFieldValue).toHaveBeenNthCalledWith(1, 'scope');
  expect(props.form.getFieldValue).toHaveBeenNthCalledWith(2, 'scoping');
});
