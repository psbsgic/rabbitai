
import { AdhocFilter, DataMask } from '@rabbitai-ui/core';
import { Scope } from '../types';

export interface NativeFiltersFormItem {
  scope: Scope;
  name: string;
  filterType: string;
  dataset: {
    value: number;
    label: string;
  };
  column: string;
  controlValues: {
    [key: string]: any;
  };
  defaultValue: any;
  defaultDataMask: DataMask;
  parentFilter: {
    value: string;
    label: string;
  };
  sortMetric: string | null;
  isInstant: boolean;
  adhoc_filters?: AdhocFilter[];
  time_range?: string;
}

export interface NativeFiltersForm {
  filters: Record<string, NativeFiltersFormItem>;
}

export type FilterRemoval =
  | null
  | {
      isPending: true; // the filter sticks around for a moment before removal is finalized
      timerId: number; // id of the timer that finally removes the filter
    }
  | { isPending: false };
