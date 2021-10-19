import { DataMask } from '@superset-ui/core';

export enum DataMaskType {
  NativeFilters = 'nativeFilters',
  CrossFilters = 'crossFilters',
}

export type DataMaskState = { [id: string]: DataMask };

export type DataMaskWithId = { id: string } & DataMask;
export type DataMaskStateWithId = { [filterId: string]: DataMaskWithId };
