/* eslint-disable import/prefer-default-export */
import { DatasourceType } from '@superset-ui/core';
import { Datasource } from 'src/dashboard/types';
export const PLACEHOLDER_DATASOURCE: Datasource = {
  id: 0,
  type: DatasourceType.Table,
  uid: '_placeholder_',
  datasource_name: '',
  table_name: '',
  columns: [],
  column_types: [],
  metrics: [],
  column_format: {},
  verbose_map: {},
  main_dttm_col: '',
  description: '',
};
