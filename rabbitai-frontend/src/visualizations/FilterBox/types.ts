import { ChartProps, Datasource } from '@superset-ui/core';

export interface FilterConfig {
  column: string;
  label: string;
}

export type FilterBoxChartProps = ChartProps & {
  datasource?: Datasource;
  formData: ChartProps['formData'] & { filterConfigs: FilterConfig[] };
};
