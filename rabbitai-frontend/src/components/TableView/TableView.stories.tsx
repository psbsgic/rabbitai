
import React from 'react';
import TableView, { TableViewProps, EmptyWrapperType } from '.';

export default {
  title: 'TableView',
  component: TableView,
};

export const InteractiveTableView = (args: TableViewProps) => (
  <TableView {...args} />
);

InteractiveTableView.args = {
  columns: [
    {
      accessor: 'id',
      Header: 'ID',
      sortable: true,
    },
    {
      accessor: 'age',
      Header: 'Age',
    },
    {
      accessor: 'name',
      Header: 'Name',
    },
  ],
  data: [
    { id: 123, age: 27, name: 'Emily' },
    { id: 321, age: 10, name: 'Kate' },
  ],
  initialSortBy: [{ id: 'name', desc: true }],
  noDataText: 'No data here',
  pageSize: 1,
  showRowCount: true,
  withPagination: true,
};

InteractiveTableView.argTypes = {
  emptyWrapperType: {
    control: {
      type: 'select',
      options: [EmptyWrapperType.Default, EmptyWrapperType.Small],
    },
  },
  pageSize: {
    control: {
      type: 'number',
      min: 1,
    },
  },
  initialPageIndex: {
    control: {
      type: 'number',
      min: 0,
    },
  },
};

InteractiveTableView.story = {
  parameters: {
    knobs: {
      disable: true,
    },
  },
};
