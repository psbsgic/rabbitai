/* eslint-disable no-param-reassign */
import { CHART_TYPE } from './componentTypes';

export default function getLayoutComponentFromChartId(layout, chartId) {
  return Object.values(layout).find(
    currentComponent =>
      currentComponent &&
      currentComponent.type === CHART_TYPE &&
      currentComponent.meta &&
      currentComponent.meta.chartId === chartId,
  );
}
