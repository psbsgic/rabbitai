

import { DataMask } from '@rabbitai-ui/core';
import { Filter } from '../../types';

export type CascadeFilter = Filter & { dataMask?: DataMask } & {
  cascadeChildren: CascadeFilter[];
};
