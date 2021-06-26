
import React from 'react';
import { DataMask } from '@rabbitai-ui/core';
import { Filter } from '../../types';

export interface FilterProps {
  filter: Filter & {
    dataMask?: DataMask;
  };
  icon?: React.ReactElement;
  directPathToChild?: string[];
  onFilterSelectionChange: (filter: Filter, dataMask: DataMask) => void;
}
