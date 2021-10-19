import React, { useEffect } from 'react';
import isEqual from 'lodash/isEqual';
import { styled, t } from '@superset-ui/core';
import { useFilters, usePagination, useSortBy, useTable } from 'react-table';
import { Empty } from 'src/common/components';
import { TableCollection, Pagination } from 'src/components/dataViewCommon';
import { SortByType, ServerPagination } from './types';

const DEFAULT_PAGE_SIZE = 10;

export enum EmptyWrapperType {
  Default = 'Default',
  Small = 'Small',
}

export interface TableViewProps {
  columns: any[];
  data: any[];
  pageSize?: number;
  totalCount?: number;
  serverPagination?: boolean;
  onServerPagination?: (args: ServerPagination) => void;
  initialPageIndex?: number;
  initialSortBy?: SortByType;
  loading?: boolean;
  withPagination?: boolean;
  emptyWrapperType?: EmptyWrapperType;
  noDataText?: string;
  className?: string;
  isPaginationSticky?: boolean;
  showRowCount?: boolean;
  scrollTable?: boolean;
  small?: boolean;
}

const EmptyWrapper = styled.div`
  margin: ${({ theme }) => theme.gridUnit * 40}px 0;
`;

const TableViewStyles = styled.div<{
  isPaginationSticky?: boolean;
  scrollTable?: boolean;
  small?: boolean;
}>`
  ${({ scrollTable, theme }) =>
    scrollTable &&
    `
    height: 380px;
    margin-bottom: ${theme.gridUnit * 4}px;
    overflow: auto;
  `}

  .table-row {
    ${({ theme, small }) => !small && `height: ${theme.gridUnit * 11 - 1}px;`}

    .table-cell {
      ${({ theme, small }) =>
        small &&
        `
        padding-top: ${theme.gridUnit + 1}px;
        padding-bottom: ${theme.gridUnit + 1}px;
        line-height: 1.45;
      `}
    }
  }

  th[role='columnheader'] {
    z-index: 1;
    border-bottom: ${({ theme }) =>
      `${theme.gridUnit - 2}px solid ${theme.colors.grayscale.light2}`};
    ${({ small }) => small && `padding-bottom: 0;`}
  }

  .pagination-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background-color: ${({ theme }) => theme.colors.grayscale.light5};

    ${({ isPaginationSticky }) =>
      isPaginationSticky &&
      `
        position: sticky;
        bottom: 0;
        left: 0;
    `};
  }

  .row-count-container {
    margin-top: ${({ theme }) => theme.gridUnit * 2}px;
    color: ${({ theme }) => theme.colors.grayscale.base};
  }
`;

const TableView = ({
  columns,
  data,
  pageSize: initialPageSize,
  totalCount = data.length,
  initialPageIndex,
  initialSortBy = [],
  loading = false,
  withPagination = true,
  emptyWrapperType = EmptyWrapperType.Default,
  noDataText,
  showRowCount = true,
  serverPagination = false,
  onServerPagination = () => {},
  ...props
}: TableViewProps) => {
  const initialState = {
    pageSize: initialPageSize ?? DEFAULT_PAGE_SIZE,
    pageIndex: initialPageIndex ?? 0,
    sortBy: initialSortBy,
  };

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    page,
    rows,
    prepareRow,
    pageCount,
    gotoPage,
    state: { pageIndex, pageSize, sortBy },
  } = useTable(
    {
      columns,
      data,
      initialState,
      manualPagination: serverPagination,
      manualSortBy: serverPagination,
      pageCount: Math.ceil(totalCount / initialState.pageSize),
    },
    useFilters,
    useSortBy,
    usePagination,
  );

  useEffect(() => {
    if (serverPagination && pageIndex !== initialState.pageIndex) {
      onServerPagination({
        pageIndex,
      });
    }
  }, [pageIndex]);

  useEffect(() => {
    if (serverPagination && !isEqual(sortBy, initialState.sortBy)) {
      onServerPagination({
        pageIndex: 0,
        sortBy,
      });
    }
  }, [sortBy]);

  const content = withPagination ? page : rows;

  let EmptyWrapperComponent;
  switch (emptyWrapperType) {
    case EmptyWrapperType.Small:
      EmptyWrapperComponent = ({ children }: any) => <>{children}</>;
      break;
    case EmptyWrapperType.Default:
    default:
      EmptyWrapperComponent = ({ children }: any) => (
        <EmptyWrapper>{children}</EmptyWrapper>
      );
  }

  const isEmpty = !loading && content.length === 0;

  return (
    <TableViewStyles {...props}>
      <TableCollection
        getTableProps={getTableProps}
        getTableBodyProps={getTableBodyProps}
        prepareRow={prepareRow}
        headerGroups={headerGroups}
        rows={content}
        columns={columns}
        loading={loading}
      />
      {isEmpty && (
        <EmptyWrapperComponent>
          {noDataText ? (
            <Empty
              image={Empty.PRESENTED_IMAGE_SIMPLE}
              description={noDataText}
            />
          ) : (
            <Empty image={Empty.PRESENTED_IMAGE_SIMPLE} />
          )}
        </EmptyWrapperComponent>
      )}
      {pageCount > 1 && withPagination && (
        <div className="pagination-container">
          <Pagination
            totalPages={pageCount || 0}
            currentPage={pageCount ? pageIndex + 1 : 0}
            onChange={(p: number) => gotoPage(p - 1)}
            hideFirstAndLastPageLinks
          />
          {showRowCount && (
            <div className="row-count-container">
              {!loading &&
                t(
                  '%s-%s of %s',
                  pageSize * pageIndex + (page.length && 1),
                  pageSize * pageIndex + page.length,
                  totalCount,
                )}
            </div>
          )}
        </div>
      )}
    </TableViewStyles>
  );
};

export default React.memo(TableView);
