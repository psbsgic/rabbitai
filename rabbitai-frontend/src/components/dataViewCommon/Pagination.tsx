import React from 'react';
import Pagination from 'src/components/Pagination';
import {
  createUltimatePagination,
  ITEM_TYPES,
} from 'react-ultimate-pagination';

const ListViewPagination = createUltimatePagination({
  WrapperComponent: Pagination,
  itemTypeToComponent: {
    [ITEM_TYPES.PAGE]: ({ value, isActive, onClick }) => (
      <Pagination.Item active={isActive} onClick={onClick}>
        {value}
      </Pagination.Item>
    ),
    [ITEM_TYPES.ELLIPSIS]: ({ isActive, onClick }) => (
      <Pagination.Ellipsis disabled={isActive} onClick={onClick} />
    ),
    [ITEM_TYPES.PREVIOUS_PAGE_LINK]: ({ isActive, onClick }) => (
      <Pagination.Prev disabled={isActive} onClick={onClick} />
    ),
    [ITEM_TYPES.NEXT_PAGE_LINK]: ({ isActive, onClick }) => (
      <Pagination.Next disabled={isActive} onClick={onClick} />
    ),
    [ITEM_TYPES.FIRST_PAGE_LINK]: () => null,
    [ITEM_TYPES.LAST_PAGE_LINK]: () => null,
  },
});

export default ListViewPagination;
