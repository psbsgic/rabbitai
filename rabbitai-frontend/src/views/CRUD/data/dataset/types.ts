
type ColumnObject = {
  id: number;
  column_name: string;
  type: string;
  verbose_name?: string;
  description?: string;
  expression?: string;
  filterable: boolean;
  groupby: boolean;
  is_active: boolean;
  is_dttm: boolean;
  python_date_format?: string;
  uuid?: string;
};

type MetricObject = {
  id: number;
  expression?: string;
  description?: string;
  metric_name: string;
  metric_type: string;
  d3format?: string;
  warning_text?: string;
};

export type DatasetObject = {
  table_name?: string;
  sql?: string;
  filter_select_enabled?: boolean;
  fetch_values_predicate?: string;
  schema?: string;
  description?: string;
  main_dttm_col?: string;
  offset?: number;
  default_endpoint?: string;
  cache_timeout?: number;
  is_sqllab_view?: boolean;
  template_params?: string;
  owners: number[];
  columns: ColumnObject[];
  metrics: MetricObject[];
  extra?: string;
};
