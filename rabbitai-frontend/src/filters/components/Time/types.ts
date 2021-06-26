
import {
  Behavior,
  DataRecord,
  FilterState,
  QueryFormData,
} from '@rabbitai-ui/core';
import { PluginFilterHooks, PluginFilterStylesProps } from '../types';

interface PluginFilterTimeCustomizeProps {
  defaultValue?: string | null;
}

export type PluginFilterSelectQueryFormData = QueryFormData &
  PluginFilterStylesProps &
  PluginFilterTimeCustomizeProps;

export type PluginFilterTimeProps = PluginFilterStylesProps & {
  behaviors: Behavior[];
  data: DataRecord[];
  formData: PluginFilterSelectQueryFormData;
  filterState: FilterState;
} & PluginFilterHooks;

export const DEFAULT_FORM_DATA: PluginFilterTimeCustomizeProps = {
  defaultValue: null,
};
