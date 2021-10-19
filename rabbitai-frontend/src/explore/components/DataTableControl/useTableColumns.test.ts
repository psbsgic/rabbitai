import { renderHook } from '@testing-library/react-hooks';
import { BOOL_FALSE_DISPLAY, BOOL_TRUE_DISPLAY } from 'src/constants';
import { useTableColumns } from '.';

// eslint-disable-next-line @typescript-eslint/no-explicit-any
type JsonObject = { [member: string]: any };

const asciiChars = [];
for (let i = 32; i < 127; i += 1) {
  asciiChars.push(String.fromCharCode(i));
}
const asciiKey = asciiChars.join('');
const unicodeKey = '你好. 吃了吗?';

const data = [
  { col01: true, col02: false, [asciiKey]: asciiKey, [unicodeKey]: unicodeKey },
  { col01: true, col02: false, [asciiKey]: asciiKey, [unicodeKey]: unicodeKey },
  { col01: true, col02: false, [asciiKey]: asciiKey, [unicodeKey]: unicodeKey },
  {
    col01: true,
    col02: false,
    col03: 'secret',
    [asciiKey]: asciiKey,
    [unicodeKey]: unicodeKey,
  },
];

test('useTableColumns with no options', () => {
  const hook = renderHook(() => useTableColumns(data));
  expect(hook.result.current).toEqual([
    {
      Cell: expect.any(Function),
      Header: 'col01',
      accessor: expect.any(Function),
    },
    {
      Cell: expect.any(Function),
      Header: 'col02',
      accessor: expect.any(Function),
    },
    {
      Cell: expect.any(Function),
      Header: asciiKey,
      accessor: expect.any(Function),
    },
    {
      Cell: expect.any(Function),
      Header: unicodeKey,
      accessor: expect.any(Function),
    },
  ]);
  hook.result.current.forEach((col: JsonObject) => {
    expect(col.accessor(data[0])).toBe(data[0][col.Header]);
  });

  hook.result.current.forEach((col: JsonObject) => {
    data.forEach(row => {
      expect(col.Cell({ value: row.col01 })).toBe(BOOL_TRUE_DISPLAY);
      expect(col.Cell({ value: row.col02 })).toBe(BOOL_FALSE_DISPLAY);
      expect(col.Cell({ value: row[asciiKey] })).toBe(asciiKey);
      expect(col.Cell({ value: row[unicodeKey] })).toBe(unicodeKey);
    });
  });
});

test('use only the first record columns', () => {
  const newData = [data[3], data[0]];
  const hook = renderHook(() => useTableColumns(newData));
  expect(hook.result.current).toEqual([
    {
      Cell: expect.any(Function),
      Header: 'col01',
      accessor: expect.any(Function),
    },
    {
      Cell: expect.any(Function),
      Header: 'col02',
      accessor: expect.any(Function),
    },
    {
      Cell: expect.any(Function),
      Header: 'col03',
      accessor: expect.any(Function),
    },
    {
      Cell: expect.any(Function),
      Header: asciiKey,
      accessor: expect.any(Function),
    },
    {
      Cell: expect.any(Function),
      Header: unicodeKey,
      accessor: expect.any(Function),
    },
  ]);

  hook.result.current.forEach((col: JsonObject) => {
    expect(col.accessor(newData[0])).toBe(newData[0][col.Header]);
  });

  hook.result.current.forEach((col: JsonObject) => {
    expect(col.Cell({ value: newData[0].col01 })).toBe(BOOL_TRUE_DISPLAY);
    expect(col.Cell({ value: newData[0].col02 })).toBe(BOOL_FALSE_DISPLAY);
    expect(col.Cell({ value: newData[0].col03 })).toBe('secret');
    expect(col.Cell({ value: newData[0][asciiKey] })).toBe(asciiKey);
    expect(col.Cell({ value: newData[0][unicodeKey] })).toBe(unicodeKey);
  });

  hook.result.current.forEach((col: JsonObject) => {
    expect(col.Cell({ value: newData[1].col01 })).toBe(BOOL_TRUE_DISPLAY);
    expect(col.Cell({ value: newData[1].col02 })).toBe(BOOL_FALSE_DISPLAY);
    expect(col.Cell({ value: newData[1].col03 })).toBe('undefined');
    expect(col.Cell({ value: newData[1][asciiKey] })).toBe(asciiKey);
    expect(col.Cell({ value: newData[1][unicodeKey] })).toBe(unicodeKey);
  });
});

test('useTableColumns with options', () => {
  const hook = renderHook(() => useTableColumns(data, { col01: { id: 'ID' } }));
  expect(hook.result.current).toEqual([
    {
      Cell: expect.any(Function),
      Header: 'col01',
      accessor: expect.any(Function),
      id: 'ID',
    },
    {
      Cell: expect.any(Function),
      Header: 'col02',
      accessor: expect.any(Function),
    },
    {
      Cell: expect.any(Function),
      Header: asciiKey,
      accessor: expect.any(Function),
    },
    {
      Cell: expect.any(Function),
      Header: unicodeKey,
      accessor: expect.any(Function),
    },
  ]);
  hook.result.current.forEach((col: JsonObject) => {
    expect(col.accessor(data[0])).toBe(data[0][col.Header]);
  });

  hook.result.current.forEach((col: JsonObject) => {
    data.forEach(row => {
      expect(col.Cell({ value: row.col01 })).toBe(BOOL_TRUE_DISPLAY);
      expect(col.Cell({ value: row.col02 })).toBe(BOOL_FALSE_DISPLAY);
      expect(col.Cell({ value: row[asciiKey] })).toBe(asciiKey);
      expect(col.Cell({ value: row[unicodeKey] })).toBe(unicodeKey);
    });
  });
});
