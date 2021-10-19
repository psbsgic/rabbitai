import { Behavior, ChartMetadata, ChartPlugin, t } from '@superset-ui/core';
import buildQuery from './buildQuery';
import controlPanel from './controlPanel';
import transformProps from './transformProps';
import thumbnail from './images/thumbnail.png';

export default class RangeFilterPlugin extends ChartPlugin {
  constructor() {
    const metadata = new ChartMetadata({
      name: t('Range filter'),
      description: t('Range filter plugin using AntD'),
      behaviors: [Behavior.INTERACTIVE_CHART, Behavior.NATIVE_FILTER],
      thumbnail,
    });

    super({
      buildQuery,
      controlPanel,
      loadChart: () => import('./RangeFilterPlugin'),
      metadata,
      transformProps,
    });
  }
}
