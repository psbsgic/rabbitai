import React from 'react';
import { DataMask } from '@superset-ui/core';
import { DataMaskStateWithId } from 'src/dataMask/types';
import { Filter } from '../../types';

export interface FilterProps {
  dataMaskSelected?: DataMaskStateWithId;
  filter: Filter & {
    dataMask?: DataMask;
  };
  icon?: React.ReactElement;
  directPathToChild?: string[];
  onFilterSelectionChange: (filter: Filter, dataMask: DataMask) => void;
  inView?: boolean;
}
