import { ChartProps } from '@superset-ui/core';
import { DEFAULT_FORM_DATA } from './types';

export default function transformProps(chartProps: ChartProps) {
  const {
    behaviors,
    formData,
    height,
    hooks,
    queriesData,
    width,
    filterState,
  } = chartProps;
  const {
    setDataMask = () => {},
    setFocusedFilter = () => {},
    unsetFocusedFilter = () => {},
  } = hooks;

  const { data } = queriesData[0];

  return {
    filterState,
    behaviors,
    width,
    height,
    data,
    formData: { ...DEFAULT_FORM_DATA, ...formData },
    setDataMask,
    setFocusedFilter,
    unsetFocusedFilter,
  };
}
