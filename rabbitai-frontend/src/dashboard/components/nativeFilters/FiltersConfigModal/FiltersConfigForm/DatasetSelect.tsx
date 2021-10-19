import React, { useCallback, useMemo } from 'react';
import rison from 'rison';
import { t, SupersetClient } from '@superset-ui/core';
import { Select } from 'src/components';
import { cacheWrapper } from 'src/utils/cacheWrapper';
import {
  ClientErrorObject,
  getClientErrorObject,
} from 'src/utils/getClientErrorObject';
import { datasetToSelectOption } from './utils';

const localCache = new Map<string, any>();

const cachedSupersetGet = cacheWrapper(
  SupersetClient.get,
  localCache,
  ({ endpoint }) => endpoint || '',
);

interface DatasetSelectProps {
  onChange: (value: { label: string; value: number }) => void;
  value?: { label: string; value: number };
}

const DatasetSelect = ({ onChange, value }: DatasetSelectProps) => {
  const getErrorMessage = useCallback(
    ({ error, message }: ClientErrorObject) => {
      let errorText = message || error || t('An error has occurred');
      if (message === 'Forbidden') {
        errorText = t('You do not have permission to edit this dashboard');
      }
      return errorText;
    },
    [],
  );

  const loadDatasetOptions = async (
    search: string,
    page: number,
    pageSize: number,
  ) => {
    const searchColumn = 'table_name';
    const query = rison.encode({
      filters: [{ col: searchColumn, opr: 'ct', value: search }],
      page,
      page_size: pageSize,
      order_column: searchColumn,
      order_direction: 'asc',
    });
    return cachedSupersetGet({
      endpoint: `/api/v1/dataset/?q=${query}`,
    })
      .then(response => {
        const data: {
          label: string;
          value: string | number;
        }[] = response.json.result
          .map(datasetToSelectOption)
          .sort((a: { label: string }, b: { label: string }) =>
            a.label.localeCompare(b.label),
          );
        return {
          data,
          totalCount: response.json.count,
        };
      })
      .catch(async error => {
        const errorMessage = getErrorMessage(await getClientErrorObject(error));
        throw new Error(errorMessage);
      });
  };

  return (
    <Select
      ariaLabel={t('Dataset')}
      value={value}
      options={loadDatasetOptions}
      onChange={onChange}
    />
  );
};

const MemoizedSelect = (props: DatasetSelectProps) =>
  // eslint-disable-next-line react-hooks/exhaustive-deps
  useMemo(() => <DatasetSelect {...props} />, []);

export default MemoizedSelect;
