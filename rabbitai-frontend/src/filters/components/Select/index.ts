
import { Behavior, ChartMetadata, ChartPlugin, t } from '@rabbitai-ui/core';
import buildQuery from './buildQuery';
import controlPanel from './controlPanel';
import transformProps from './transformProps';
import thumbnail from './images/thumbnail.png';

export default class FilterSelectPlugin extends ChartPlugin {
  constructor() {
    const metadata = new ChartMetadata({
      name: t('Select filter'),
      description: t('Select filter plugin using AntD'),
      behaviors: [Behavior.INTERACTIVE_CHART, Behavior.NATIVE_FILTER],
      enableNoResults: false,
      thumbnail,
    });

    super({
      buildQuery,
      controlPanel,
      loadChart: () => import('./SelectFilterPlugin'),
      metadata,
      transformProps,
    });
  }
}
