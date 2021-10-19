import { DataMask } from '@superset-ui/core';
import { Filter } from '../../types';

export type CascadeFilter = Filter & { dataMask?: DataMask } & {
  cascadeChildren: CascadeFilter[];
};
