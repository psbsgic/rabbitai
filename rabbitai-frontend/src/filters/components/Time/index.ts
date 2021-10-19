import { Behavior, ChartMetadata, ChartPlugin, t } from '@superset-ui/core';
import controlPanel from './controlPanel';
import transformProps from './transformProps';
import thumbnail from './images/thumbnail.png';

export default class TimeFilterPlugin extends ChartPlugin {
  constructor() {
    const metadata = new ChartMetadata({
      name: t('Time filter'),
      description: t('Custom time filter plugin'),
      behaviors: [Behavior.INTERACTIVE_CHART, Behavior.NATIVE_FILTER],
      thumbnail,
      datasourceCount: 0,
    });

    super({
      controlPanel,
      loadChart: () => import('./TimeFilterPlugin'),
      metadata,
      transformProps,
    });
  }
}
