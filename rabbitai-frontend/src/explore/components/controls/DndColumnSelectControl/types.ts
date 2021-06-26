
import { ReactNode } from 'react';
import { Metric } from '@rabbitai-ui/core';
import { ColumnMeta } from '@rabbitai-ui/chart-controls';
import { DatasourcePanelDndItem } from '../../DatasourcePanel/types';
import { DndItemType } from '../../DndItemType';

export interface OptionProps {
  children: ReactNode;
  index: number;
  clickClose: (index: number) => void;
  withCaret?: boolean;
}

export interface OptionItemInterface {
  type: string;
  dragIndex: number;
}

export interface LabelProps<T = string[] | string> {
  name: string;
  value?: T;
  onChange: (value?: T) => void;
  options: { string: ColumnMeta };
  multi?: boolean;
}

export interface DndColumnSelectProps<
  T = string[] | string,
  O = string[] | string
> extends LabelProps<T> {
  onDrop: (item: DatasourcePanelDndItem) => void;
  canDrop: (item: DatasourcePanelDndItem) => boolean;
  valuesRenderer: () => ReactNode;
  accept: DndItemType | DndItemType[];
  ghostButtonText?: string;
  displayGhostButton?: boolean;
}

export type OptionValueType = Record<string, any>;
export interface DndFilterSelectProps {
  name: string;
  value: OptionValueType[];
  columns: ColumnMeta[];
  datasource: Record<string, any>;
  formData: Record<string, any>;
  savedMetrics: Metric[];
  onChange: (filters: OptionValueType[]) => void;
  options: { string: ColumnMeta };
}
