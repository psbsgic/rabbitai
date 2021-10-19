import { FilterBoxChartProps } from './types';

const NOOP = () => {};

export default function transformProps(chartProps: FilterBoxChartProps) {
  const {
    datasource,
    formData,
    hooks,
    initialValues,
    queriesData,
    rawDatasource = {},
    rawFormData,
    width,
    height,
  } = chartProps;
  const {
    onAddFilter = NOOP,
    onFilterMenuOpen = NOOP,
    onFilterMenuClose = NOOP,
  } = hooks;
  const {
    sliceId,
    dateFilter,
    instantFiltering,
    showDruidTimeGranularity,
    showDruidTimeOrigin,
    showSqlaTimeColumn,
    showSqlaTimeGranularity,
  } = formData;
  const { verboseMap = {} } = datasource;
  const filterConfigs = formData.filterConfigs || [];

  const filtersFields = filterConfigs.map(flt => ({
    ...flt,
    key: flt.column,
    label: flt.label || verboseMap[flt.column] || flt.column,
  }));

  return {
    chartId: sliceId,
    width,
    height,
    datasource: rawDatasource,
    filtersChoices: queriesData[0].data,
    filtersFields,
    instantFiltering,
    onChange: onAddFilter,
    onFilterMenuOpen,
    onFilterMenuClose,
    origSelectedValues: initialValues || {},
    showDateFilter: dateFilter,
    showDruidTimeGrain: showDruidTimeGranularity,
    showDruidTimeOrigin,
    showSqlaTimeColumn,
    showSqlaTimeGrain: showSqlaTimeGranularity,
    // the original form data, needed for async select options
    rawFormData,
  };
}
