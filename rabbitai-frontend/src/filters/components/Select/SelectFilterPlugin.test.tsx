import userEvent from '@testing-library/user-event';
import { AppSection } from '@superset-ui/core';
import React from 'react';
import { render, screen } from 'spec/helpers/testing-library';
import SelectFilterPlugin from './SelectFilterPlugin';
import transformProps from './transformProps';

const selectMultipleProps = {
  formData: {
    sortAscending: true,
    multiSelect: true,
    enableEmptyFilter: true,
    defaultToFirstItem: false,
    inverseSelection: false,
    searchAllOptions: false,
    datasource: '3__table',
    groupby: ['gender'],
    adhocFilters: [],
    extraFilters: [],
    extraFormData: {},
    granularitySqla: 'ds',
    metrics: ['count'],
    rowLimit: 1000,
    showSearch: true,
    defaultValue: ['boy'],
    timeRangeEndpoints: ['inclusive', 'exclusive'],
    urlParams: {},
    vizType: 'filter_select',
    inputRef: { current: null },
  },
  height: 20,
  hooks: {},
  ownState: {},
  filterState: { value: ['boy'] },
  queriesData: [
    {
      rowcount: 2,
      colnames: ['gender'],
      coltypes: [1],
      data: [{ gender: 'boy' }, { gender: 'girl' }],
      applied_filters: [{ column: 'gender' }],
      rejected_filters: [],
    },
  ],
  width: 220,
  behaviors: ['NATIVE_FILTER'],
  isRefreshing: false,
  appSection: AppSection.DASHBOARD,
};

describe('SelectFilterPlugin', () => {
  const setDataMask = jest.fn();
  const getWrapper = (props = {}) =>
    render(
      // @ts-ignore
      <SelectFilterPlugin
        // @ts-ignore
        {...transformProps({
          ...selectMultipleProps,
          formData: { ...selectMultipleProps.formData, ...props },
        })}
        setDataMask={setDataMask}
      />,
    );

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('Add multiple values with first render', () => {
    getWrapper();
    expect(setDataMask).toHaveBeenCalledWith({
      extraFormData: {},
      filterState: {
        value: ['boy'],
      },
    });
    expect(setDataMask).toHaveBeenCalledWith({
      __cache: {
        value: ['boy'],
      },
      extraFormData: {
        filters: [
          {
            col: 'gender',
            op: 'IN',
            val: ['boy'],
          },
        ],
      },
      filterState: {
        label: 'boy',
        value: ['boy'],
      },
    });
    userEvent.click(screen.getByRole('combobox'));
    userEvent.click(screen.getByTitle('girl'));
    expect(setDataMask).toHaveBeenCalledWith({
      __cache: {
        value: ['boy'],
      },
      extraFormData: {
        filters: [
          {
            col: 'gender',
            op: 'IN',
            val: ['boy', 'girl'],
          },
        ],
      },
      filterState: {
        label: 'boy, girl',
        value: ['boy', 'girl'],
      },
    });
  });

  it('Remove multiple values when required', () => {
    getWrapper();
    userEvent.click(document.querySelector('[data-icon="close"]')!);
    expect(setDataMask).toHaveBeenCalledWith({
      __cache: {
        value: ['boy'],
      },
      extraFormData: {
        adhoc_filters: [
          {
            clause: 'WHERE',
            expressionType: 'SQL',
            sqlExpression: '1 = 0',
          },
        ],
      },
      filterState: {
        label: undefined,
        value: null,
      },
    });
  });

  it('Remove multiple values when not required', () => {
    getWrapper({ enableEmptyFilter: false });
    userEvent.click(document.querySelector('[data-icon="close"]')!);
    expect(setDataMask).toHaveBeenCalledWith({
      __cache: {
        value: ['boy'],
      },
      extraFormData: {},
      filterState: {
        label: undefined,
        value: null,
      },
    });
  });

  it('Select single values with inverse', () => {
    getWrapper({ multiSelect: false, inverseSelection: true });
    userEvent.click(screen.getByRole('combobox'));
    userEvent.click(screen.getByTitle('girl'));
    expect(setDataMask).toHaveBeenCalledWith({
      __cache: {
        value: ['boy'],
      },
      extraFormData: {
        filters: [
          {
            col: 'gender',
            op: 'NOT IN',
            val: ['girl'],
          },
        ],
      },
      filterState: {
        label: 'girl (excluded)',
        value: ['girl'],
      },
    });
  });

  it('Add ownState with column types when search all options', () => {
    getWrapper({ searchAllOptions: true, multiSelect: false });
    userEvent.click(screen.getByRole('combobox'));
    userEvent.click(screen.getByTitle('girl'));
    expect(setDataMask).toHaveBeenCalledWith({
      __cache: {
        value: ['boy'],
      },
      extraFormData: {
        filters: [
          {
            col: 'gender',
            op: 'IN',
            val: ['girl'],
          },
        ],
      },
      filterState: {
        label: 'girl',
        value: ['girl'],
      },
      ownState: {
        coltypeMap: {
          gender: 1,
        },
        search: null,
      },
    });
  });
});
