import { ColumnMeta, Metric } from '@superset-ui/chart-controls';
import { DndItemType } from '../DndItemType';

export type DndItemValue = ColumnMeta | Metric;

export interface DatasourcePanelDndItem {
  value: DndItemValue;
  type: DndItemType;
}
