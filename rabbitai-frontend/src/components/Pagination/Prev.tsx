import React from 'react';
import classNames from 'classnames';
import { PaginationButtonProps } from './types';

export function Prev({ disabled, onClick }: PaginationButtonProps) {
  return (
    <li className={classNames({ disabled })}>
      <span
        role="button"
        tabIndex={disabled ? -1 : 0}
        onClick={e => {
          e.preventDefault();
          if (!disabled) onClick(e);
        }}
      >
        «
      </span>
    </li>
  );
}
