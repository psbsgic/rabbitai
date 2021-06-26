

import React from 'react';
import { styled } from '@rabbitai-ui/core';
import { Next } from './Next';
import { Prev } from './Prev';
import { Item } from './Item';
import { Ellipsis } from './Ellipsis';

interface PaginationProps {
  children: JSX.Element | JSX.Element[];
}

const PaginationList = styled.ul`
  display: inline-block;
  margin: 16px 0;
  padding: 0;

  li {
    display: inline;
    margin: 0 4px;

    span {
      padding: 8px 12px;
      text-decoration: none;
      background-color: ${({ theme }) => theme.colors.grayscale.light5};
      border-radius: ${({ theme }) => theme.borderRadius}px;

      &:hover,
      &:focus {
        z-index: 2;
        color: ${({ theme }) => theme.colors.grayscale.dark1};
        background-color: ${({ theme }) => theme.colors.grayscale.light3};
      }
    }

    &.disabled {
      span {
        background-color: transparent;
        cursor: default;

        &:focus {
          outline: none;
        }
      }
    }
    &.active {
      span {
        z-index: 3;
        color: ${({ theme }) => theme.colors.grayscale.light5};
        cursor: default;
        background-color: ${({ theme }) => theme.colors.primary.base};

        &:focus {
          outline: none;
        }
      }
    }
  }
`;

function Pagination({ children }: PaginationProps) {
  return <PaginationList role="navigation">{children}</PaginationList>;
}

Pagination.Next = Next;
Pagination.Prev = Prev;
Pagination.Item = Item;
Pagination.Ellipsis = Ellipsis;

export default Pagination;
