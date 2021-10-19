import { ReactNode } from 'react';

export enum ScopingType {
  all,
  specific,
}

/** UI Ant tree type */
export type TreeItem = {
  children: TreeItem[];
  key: string;
  title: ReactNode;
};

export type BuildTreeLeafTitle = (
  label: string,
  hasTooltip: boolean,
  tooltipTitle?: string,
) => ReactNode;
