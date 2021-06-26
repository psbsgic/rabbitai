
import { GenericDataType } from '@rabbitai-ui/core';
import { DEFAULT_FORM_DATA, PluginFilterSelectChartProps } from './types';

export default function transformProps(
  chartProps: PluginFilterSelectChartProps,
) {
  const {
    formData,
    height,
    hooks,
    queriesData,
    width,
    behaviors,
    appSection,
    filterState,
    isRefreshing,
  } = chartProps;
  const newFormData = { ...DEFAULT_FORM_DATA, ...formData };
  const {
    setDataMask = () => {},
    setFocusedFilter = () => {},
    unsetFocusedFilter = () => {},
  } = hooks;
  const [queryData] = queriesData;
  const { colnames = [], coltypes = [], data = [] } = queryData || {};
  const coltypeMap: Record<string, GenericDataType> = colnames.reduce(
    (accumulator, item, index) => ({ ...accumulator, [item]: coltypes[index] }),
    {},
  );

  return {
    filterState,
    coltypeMap,
    appSection,
    width,
    behaviors,
    height,
    data,
    formData: newFormData,
    isRefreshing,
    setDataMask,
    setFocusedFilter,
    unsetFocusedFilter,
  };
}
