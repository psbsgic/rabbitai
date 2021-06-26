
import { ChartProps } from '@rabbitai-ui/core';
import { DEFAULT_FORM_DATA } from './types';

export default function transformProps(chartProps: ChartProps) {
  const {
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
    width,
    height,
    data,
    formData: { ...DEFAULT_FORM_DATA, ...formData },
    setDataMask,
    setFocusedFilter,
    unsetFocusedFilter,
  };
}
