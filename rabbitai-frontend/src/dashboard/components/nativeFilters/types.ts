

import { AdhocFilter, DataMask } from '@rabbitai-ui/core';

export interface Column {
  name: string;
  displayName?: string;
}

export interface Scope {
  rootPath: string[];
  excluded: number[];
}

/** The target of a filter is the datasource/column being filtered */
export interface Target {
  datasetId: number;
  column: Column;

  // maybe someday support this?
  // show values from these columns in the filter options selector
  // clarityColumns?: Column[];
}

export interface Filter {
  cascadeParentIds: string[];
  defaultDataMask: DataMask;
  isInstant: boolean;
  id: string; // randomly generated at filter creation
  name: string;
  scope: Scope;
  filterType: string;
  // for now there will only ever be one target
  // when multiple targets are supported, change this to Target[]
  targets: [Partial<Target>];
  controlValues: {
    [key: string]: any;
  };
  sortMetric?: string | null;
  adhoc_filters?: AdhocFilter[];
  time_range?: string;
}

export type FilterConfiguration = Filter[];
