

import { renderHook } from '@testing-library/react-hooks';
import { useTableColumns } from '.';

const data = [
  { col01: 'some', col02: 'data' },
  { col01: 'any', col02: 'data' },
  { col01: 'some', col02: 'thing' },
  { col01: 'any', col02: 'things', col03: 'secret' },
];

test('useTableColumns with no options', () => {
  const hook = renderHook(() => useTableColumns(data));
  expect(hook.result.current).toEqual([
    { Cell: expect.any(Function), Header: 'col01', accessor: 'col01' },
    { Cell: expect.any(Function), Header: 'col02', accessor: 'col02' },
  ]);
});

test('use only the first record columns', () => {
  const hook = renderHook(() => useTableColumns(data));
  expect(hook.result.current).toEqual([
    { Cell: expect.any(Function), Header: 'col01', accessor: 'col01' },
    { Cell: expect.any(Function), Header: 'col02', accessor: 'col02' },
  ]);

  const hook2 = renderHook(() => useTableColumns([data[3], data[0]]));
  expect(hook2.result.current).toEqual([
    { Cell: expect.any(Function), Header: 'col01', accessor: 'col01' },
    { Cell: expect.any(Function), Header: 'col02', accessor: 'col02' },
    { Cell: expect.any(Function), Header: 'col03', accessor: 'col03' },
  ]);
});

test('useTableColumns with options', () => {
  const hook = renderHook(() => useTableColumns(data, { col01: { id: 'ID' } }));
  expect(hook.result.current).toEqual([
    {
      Cell: expect.any(Function),
      Header: 'col01',
      accessor: 'col01',
      id: 'ID',
    },
    { Cell: expect.any(Function), Header: 'col02', accessor: 'col02' },
  ]);
});
