import { Behavior, ChartMetadata, ChartPlugin, t } from '@superset-ui/core';
import buildQuery from './buildQuery';
import controlPanel from './controlPanel';
import transformProps from './transformProps';
import thumbnail from './images/thumbnail.png';

export default class FilterGroupByPlugin extends ChartPlugin {
  constructor() {
    const metadata = new ChartMetadata({
      name: t('Group By'),
      description: t('Group By filter plugin'),
      behaviors: [Behavior.INTERACTIVE_CHART, Behavior.NATIVE_FILTER],
      thumbnail,
    });

    super({
      buildQuery,
      controlPanel,
      loadChart: () => import('./GroupByFilterPlugin'),
      metadata,
      transformProps,
    });
  }
}
