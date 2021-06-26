
import {
  QueryData,
  QueryFormData,
  AnnotationData,
  AdhocMetric,
} from '@rabbitai-ui/core';
import { ColumnMeta } from '@rabbitai-ui/chart-controls';

export { Slice, Chart } from 'src/types/Chart';

export type ChartStatus =
  | 'loading'
  | 'rendered'
  | 'failed'
  | 'stopped'
  | 'success';

export interface ChartState {
  id: number;
  annotationData?: AnnotationData;
  annotationError?: Record<string, string>;
  annotationQuery?: Record<string, AbortController>;
  chartAlert: string | null;
  chartStatus: ChartStatus | null;
  chartStackTrace?: string | null;
  chartUpdateEndTime: number | null;
  chartUpdateStartTime: number;
  lastRendered: number;
  latestQueryFormData: Partial<QueryFormData>;
  sliceFormData: QueryFormData | null;
  queryController: AbortController | null;
  queriesResponse: QueryData | null;
  triggerQuery: boolean;
}

export type OptionSortType = Partial<
  ColumnMeta & AdhocMetric & { saved_metric_name: string }
>;
