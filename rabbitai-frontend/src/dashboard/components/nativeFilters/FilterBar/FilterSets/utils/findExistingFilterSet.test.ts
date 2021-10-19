import { FilterSet } from 'src/dashboard/reducers/types';
import { findExistingFilterSet } from '.';

const createDataMaskSelected = () => ({
  filterId: { filterState: { value: 'value-1' } },
  filterId2: { filterState: { value: 'value-2' } },
});

test('Should find correct filter', () => {
  const dataMaskSelected = createDataMaskSelected();
  const filterSetFilterValues: FilterSet[] = [
    {
      id: 'id-01',
      name: 'name-01',
      nativeFilters: {},
      dataMask: {
        filterId: { id: 'filterId', filterState: { value: 'value-1' } },
        filterId2: { id: 'filterId2', filterState: { value: 'value-2' } },
      } as any,
    },
  ];
  const response = findExistingFilterSet({
    filterSetFilterValues,
    dataMaskSelected,
  });
  expect(response).toEqual({
    dataMask: {
      filterId: { id: 'filterId', filterState: { value: 'value-1' } },
      filterId2: { id: 'filterId2', filterState: { value: 'value-2' } },
    },
    id: 'id-01',
    name: 'name-01',
    nativeFilters: {},
  });
});

test('Should return undefined when nativeFilters has less values', () => {
  const dataMaskSelected = createDataMaskSelected();
  const filterSetFilterValues = [
    {
      id: 'id-01',
      name: 'name-01',
      nativeFilters: {},
      dataMask: {
        filterId: { id: 'filterId', filterState: { value: 'value-1' } },
      } as any,
    },
  ];
  const response = findExistingFilterSet({
    filterSetFilterValues,
    dataMaskSelected,
  });
  expect(response).toBeUndefined();
});

test('Should return undefined when nativeFilters has different values', () => {
  const dataMaskSelected = createDataMaskSelected();
  const filterSetFilterValues: FilterSet[] = [
    {
      id: 'id-01',
      name: 'name-01',
      nativeFilters: {},
      dataMask: {
        filterId: { id: 'filterId', filterState: { value: 'value-1' } },
        filterId2: { id: 'filterId2', filterState: { value: 'value-1' } },
      },
    },
  ];
  const response = findExistingFilterSet({
    filterSetFilterValues,
    dataMaskSelected,
  });
  expect(response).toBeUndefined();
});

test('Should return undefined when dataMask:{}', () => {
  const dataMaskSelected = createDataMaskSelected();
  const filterSetFilterValues = [
    {
      id: 'id-01',
      name: 'name-01',
      nativeFilters: {},
      dataMask: {},
    },
  ];
  const response = findExistingFilterSet({
    filterSetFilterValues,
    dataMaskSelected,
  });
  expect(response).toBeUndefined();
});

test('Should return undefined when dataMask is empty}', () => {
  const dataMaskSelected = createDataMaskSelected();
  const filterSetFilterValues: FilterSet[] = [
    {
      id: 'id-01',
      name: 'name-01',
      nativeFilters: {},
      dataMask: {},
    },
  ];
  const response = findExistingFilterSet({
    filterSetFilterValues,
    dataMaskSelected,
  });
  expect(response).toBeUndefined();
});

test('Should return undefined when filterSetFilterValues is []', () => {
  const dataMaskSelected = createDataMaskSelected();
  const filterSetFilterValues: FilterSet[] = [];
  const response = findExistingFilterSet({
    filterSetFilterValues,
    dataMaskSelected,
  });
  expect(response).toBeUndefined();
});
