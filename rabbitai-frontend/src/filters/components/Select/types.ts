import {
  AppSection,
  Behavior,
  ChartProps,
  DataRecord,
  FilterState,
  GenericDataType,
  QueryFormData,
  ChartDataResponseResult,
} from '@superset-ui/core';
import { RefObject } from 'react';
import { PluginFilterHooks, PluginFilterStylesProps } from '../types';

export type SelectValue = (number | string)[] | null | undefined;

interface PluginFilterSelectCustomizeProps {
  defaultValue?: SelectValue;
  enableEmptyFilter: boolean;
  inverseSelection: boolean;
  multiSelect: boolean;
  defaultToFirstItem: boolean;
  inputRef?: RefObject<HTMLInputElement>;
  searchAllOptions: boolean;
  sortAscending?: boolean;
  sortMetric?: string;
}

export type PluginFilterSelectQueryFormData = QueryFormData &
  PluginFilterStylesProps &
  PluginFilterSelectCustomizeProps;

export interface PluginFilterSelectChartProps extends ChartProps {
  queriesData: ChartDataResponseResult[];
}

export type PluginFilterSelectProps = PluginFilterStylesProps & {
  coltypeMap: Record<string, GenericDataType>;
  data: DataRecord[];
  behaviors: Behavior[];
  appSection: AppSection;
  formData: PluginFilterSelectQueryFormData;
  filterState: FilterState;
  isRefreshing: boolean;
} & PluginFilterHooks;

export const DEFAULT_FORM_DATA: PluginFilterSelectCustomizeProps = {
  defaultValue: null,
  enableEmptyFilter: false,
  inverseSelection: false,
  defaultToFirstItem: false,
  multiSelect: true,
  searchAllOptions: false,
  sortAscending: true,
};
