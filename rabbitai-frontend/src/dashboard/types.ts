import { ChartProps, ExtraFormData, JsonObject } from '@rabbitai-ui/core';
import { chart } from 'src/chart/chartReducer';
import componentTypes from 'src/dashboard/util/componentTypes';
import { DataMaskStateWithId } from '../dataMask/types';
import { NativeFiltersState } from './reducers/types';
import { ChartState } from '../explore/types';

export type ChartReducerInitialState = typeof chart;

// chart query built from initialState
// Ref: https://github.com/apache/rabbitai/blob/dcac860f3e5528ecbc39e58f045c7388adb5c3d0/rabbitai-frontend/src/dashboard/reducers/getInitialState.js#L120
export interface ChartQueryPayload extends Partial<ChartReducerInitialState> {
  id: number;
  formData: ChartProps['formData'];
  form_data?: ChartProps['rawFormData'];
  [key: string]: unknown;
}

/** Chart state of redux */
export type Chart = ChartState & {
  formData: {
    viz_type: string;
  };
};

export type DashboardLayout = { [key: string]: LayoutItem };
export type DashboardLayoutState = { present: DashboardLayout };
export type DashboardState = { editMode: boolean; directPathToChild: string[] };
export type DashboardInfo = {
  common: {
    flash_messages: string[];
    conf: JsonObject;
  };
  userId: string;
  dash_edit_perm: boolean;
  metadata: { show_native_filters: boolean; chart_configuration: JsonObject };
};

export type ChartsState = { [key: string]: Chart };

/** Root state of redux */
export type RootState = {
  datasources: JsonObject;
  sliceEntities: JsonObject;
  charts: ChartsState;
  dashboardLayout: DashboardLayoutState;
  dashboardFilters: {};
  dashboardState: DashboardState;
  dashboardInfo: DashboardInfo;
  dataMask: DataMaskStateWithId;
  impressionId: string;
  nativeFilters: NativeFiltersState;
};

/** State of dashboardLayout in redux */
export type Layout = { [key: string]: LayoutItem };

/** State of charts in redux */
export type Charts = { [key: number]: Chart };

type ComponentTypesKeys = keyof typeof componentTypes;
export type ComponentType = typeof componentTypes[ComponentTypesKeys];

/** State of dashboardLayout item in redux */
export type LayoutItem = {
  children: string[];
  parents: string[];
  type: ComponentType;
  id: string;
  meta: {
    chartId: number;
    height: number;
    sliceName?: string;
    text?: string;
    uuid: string;
    width: number;
  };
};

type ActiveFilter = {
  scope: number[];
  values: ExtraFormData;
};

export type ActiveFilters = {
  [key: string]: ActiveFilter;
};
