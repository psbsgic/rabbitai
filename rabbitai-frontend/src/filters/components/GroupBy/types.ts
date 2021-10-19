import {
  Behavior,
  DataRecord,
  FilterState,
  QueryFormData,
} from '@superset-ui/core';
import { RefObject } from 'react';
import { PluginFilterHooks, PluginFilterStylesProps } from '../types';

interface PluginFilterGroupByCustomizeProps {
  defaultValue?: string[] | null;
  inputRef?: RefObject<HTMLInputElement>;
  multiSelect: boolean;
}

export type PluginFilterGroupByQueryFormData = QueryFormData &
  PluginFilterStylesProps &
  PluginFilterGroupByCustomizeProps;

export type PluginFilterGroupByProps = PluginFilterStylesProps & {
  behaviors: Behavior[];
  data: DataRecord[];
  filterState: FilterState;
  formData: PluginFilterGroupByQueryFormData;
} & PluginFilterHooks;

export const DEFAULT_FORM_DATA: PluginFilterGroupByCustomizeProps = {
  defaultValue: null,
  multiSelect: false,
};
