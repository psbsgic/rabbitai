import { SupersetError } from 'src/components/ErrorMessage/types';
import { CtasEnum } from 'src/SqlLab/actions/sqlLab';

export type Column = {
  name: string;
};

export type QueryState =
  | 'stopped'
  | 'failed'
  | 'pending'
  | 'running'
  | 'scheduled'
  | 'success'
  | 'fetching'
  | 'timed_out';

export type Query = {
  cached: boolean;
  ctas: boolean;
  ctas_method?: keyof typeof CtasEnum;
  dbId: number;
  errors?: SupersetError[];
  errorMessage: string | null;
  extra: {
    progress: string | null;
  };
  id: string;
  isDataPreview: boolean;
  link?: string;
  progress: number;
  results: {
    displayLimitReached: boolean;
    columns: Column[];
    data: Record<string, unknown>[];
    expanded_columns: Column[];
    selected_columns: Column[];
    query: { limit: number };
  };
  resultsKey: string | null;
  schema: string;
  sql: string;
  sqlEditorId: string;
  state: QueryState;
  tab: string | null;
  tempSchema: string | null;
  tempTable: string;
  trackingUrl: string | null;
  templateParams: any;
  rows: number;
  queryLimit: number;
  limitingFactor: string;
};
