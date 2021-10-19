import { ReactNode } from 'react';

export interface SortColumn {
  id: string;
  desc?: boolean;
}

export type SortColumns = SortColumn[];

export interface SelectOption {
  label: string;
  value: any;
}

export interface CardSortSelectOption {
  desc: boolean;
  id: any;
  label: string;
  value: any;
}

export interface Filter {
  Header: ReactNode;
  id: string;
  urlDisplay?: string;
  operator?: FilterOperator;
  input?:
    | 'text'
    | 'textarea'
    | 'select'
    | 'checkbox'
    | 'search'
    | 'datetime_range';
  unfilteredLabel?: string;
  selects?: SelectOption[];
  onFilterOpen?: () => void;
  fetchSelects?: (
    filterValue?: string,
    pageIndex?: number,
    pageSize?: number,
  ) => Promise<SelectOption[]>;
  paginate?: boolean;
}

export type Filters = Filter[];

export type ViewModeType = 'card' | 'table';

export interface FilterValue {
  id: string;
  urlDisplay?: string;
  operator?: string;
  value: string | boolean | number | null | undefined | string[] | number[];
}

export interface FetchDataConfig {
  pageIndex: number;
  pageSize: number;
  sortBy: SortColumns;
  filters: FilterValue[];
}

export interface InternalFilter extends FilterValue {
  Header?: string;
}

export enum FilterOperator {
  startsWith = 'sw',
  endsWith = 'ew',
  contains = 'ct',
  equals = 'eq',
  notStartsWith = 'nsw',
  notEndsWith = 'new',
  notContains = 'nct',
  notEquals = 'neq',
  greaterThan = 'gt',
  lessThan = 'lt',
  relationManyMany = 'rel_m_m',
  relationOneMany = 'rel_o_m',
  titleOrSlug = 'title_or_slug',
  nameOrDescription = 'name_or_description',
  allText = 'all_text',
  chartAllText = 'chart_all_text',
  datasetIsNullOrEmpty = 'dataset_is_null_or_empty',
  between = 'between',
  dashboardIsFav = 'dashboard_is_favorite',
  chartIsFav = 'chart_is_favorite',
}
