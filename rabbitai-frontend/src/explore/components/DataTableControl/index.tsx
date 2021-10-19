import React, { useMemo } from 'react';
import { styled, t } from '@superset-ui/core';
import { Column } from 'react-table';
import debounce from 'lodash/debounce';
import { Input } from 'src/common/components';
import {
  BOOL_FALSE_DISPLAY,
  BOOL_TRUE_DISPLAY,
  SLOW_DEBOUNCE,
} from 'src/constants';
import Button from 'src/components/Button';
import {
  applyFormattingToTabularData,
  prepareCopyToClipboardTabularData,
} from 'src/utils/common';
import CopyToClipboard from 'src/components/CopyToClipboard';
import RowCountLabel from 'src/explore/components/RowCountLabel';

export const CopyButton = styled(Button)`
  font-size: ${({ theme }) => theme.typography.sizes.s}px;

  // needed to override button's first-of-type margin: 0
  && {
    margin: 0 ${({ theme }) => theme.gridUnit * 2}px;
  }

  i {
    padding: 0 ${({ theme }) => theme.gridUnit}px;
  }
`;

const CopyNode = (
  <CopyButton buttonSize="xsmall">
    <i className="fa fa-clipboard" />
  </CopyButton>
);

export const CopyToClipboardButton = ({
  data,
}: {
  data?: Record<string, any>;
}) => (
  <CopyToClipboard
    text={data ? prepareCopyToClipboardTabularData(data) : ''}
    wrapped={false}
    copyNode={CopyNode}
  />
);

export const FilterInput = ({
  onChangeHandler,
}: {
  onChangeHandler(filterText: string): void;
}) => {
  const debouncedChangeHandler = debounce(onChangeHandler, SLOW_DEBOUNCE);
  return (
    <Input
      placeholder={t('Search')}
      onChange={(event: any) => {
        const filterText = event.target.value;
        debouncedChangeHandler(filterText);
      }}
    />
  );
};

export const RowCount = ({
  data,
  loading,
}: {
  data?: Record<string, any>[];
  loading: boolean;
}) => (
  <RowCountLabel
    rowcount={data?.length ?? 0}
    loading={loading}
    suffix={t('rows retrieved')}
  />
);

export const useFilteredTableData = (
  filterText: string,
  data?: Record<string, any>[],
) =>
  useMemo(() => {
    if (!data?.length) {
      return [];
    }
    const formattedData = applyFormattingToTabularData(data);
    return formattedData.filter((row: Record<string, any>) =>
      Object.values(row).some(value =>
        value?.toString().toLowerCase().includes(filterText.toLowerCase()),
      ),
    );
  }, [data, filterText]);

export const useTableColumns = (
  data?: Record<string, any>[],
  moreConfigs?: { [key: string]: Partial<Column> },
) =>
  useMemo(
    () =>
      data?.length
        ? Object.keys(data[0]).map(
            key =>
              ({
                accessor: row => row[key],
                Header: key,
                Cell: ({ value }) => {
                  if (value === true) {
                    return BOOL_TRUE_DISPLAY;
                  }
                  if (value === false) {
                    return BOOL_FALSE_DISPLAY;
                  }
                  return String(value);
                },
                ...moreConfigs?.[key],
              } as Column),
          )
        : [],
    [data, moreConfigs],
  );
