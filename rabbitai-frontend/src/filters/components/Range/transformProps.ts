
import { ChartProps } from '@rabbitai-ui/core';

export default function transformProps(chartProps: ChartProps) {
  const {
    formData,
    height,
    hooks,
    queriesData,
    width,
    behaviors,
    filterState,
  } = chartProps;
  const {
    setDataMask = () => {},
    setFocusedFilter = () => {},
    unsetFocusedFilter = () => {},
  } = hooks;
  const { data } = queriesData[0];

  return {
    data,
    formData,
    behaviors,
    height,
    setDataMask,
    filterState,
    width,
    setFocusedFilter,
    unsetFocusedFilter,
  };
}
