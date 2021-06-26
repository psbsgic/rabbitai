
import { FilterState, QueryFormData, DataRecord } from '@rabbitai-ui/core';
import { RefObject } from 'react';
import { PluginFilterHooks, PluginFilterStylesProps } from '../types';

interface PluginFilterTimeGrainCustomizeProps {
  defaultValue?: string[] | null;
  inputRef?: RefObject<HTMLInputElement>;
}

export type PluginFilterTimeGrainQueryFormData = QueryFormData &
  PluginFilterStylesProps &
  PluginFilterTimeGrainCustomizeProps;

export type PluginFilterTimeGrainProps = PluginFilterStylesProps & {
  data: DataRecord[];
  filterState: FilterState;
  formData: PluginFilterTimeGrainQueryFormData;
} & PluginFilterHooks;

export const DEFAULT_FORM_DATA: PluginFilterTimeGrainCustomizeProps = {
  defaultValue: null,
};
