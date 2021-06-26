
import {
  Behavior,
  DataRecord,
  FilterState,
  QueryFormData,
} from '@rabbitai-ui/core';
import { RefObject } from 'react';
import { PluginFilterHooks, PluginFilterStylesProps } from '../types';

interface PluginFilterSelectCustomizeProps {
  max?: number;
  min?: number;
}

export type PluginFilterRangeQueryFormData = QueryFormData &
  PluginFilterStylesProps &
  PluginFilterSelectCustomizeProps;

export type PluginFilterRangeProps = PluginFilterStylesProps & {
  data: DataRecord[];
  formData: PluginFilterRangeQueryFormData;
  filterState: FilterState;
  behaviors: Behavior[];
  inputRef: RefObject<any>;
} & PluginFilterHooks;
