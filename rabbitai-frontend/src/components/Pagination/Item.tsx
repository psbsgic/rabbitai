

import React from 'react';
import classNames from 'classnames';
import { PaginationButtonProps } from './types';

interface PaginationItemButton extends PaginationButtonProps {
  active?: boolean;
  children: React.ReactNode;
}

export function Item({ active, children, onClick }: PaginationItemButton) {
  return (
    <li className={classNames({ active })}>
      <span
        role="button"
        tabIndex={active ? -1 : 0}
        onClick={e => {
          e.preventDefault();
          if (!active) onClick(e);
        }}
      >
        {children}
      </span>
    </li>
  );
}
