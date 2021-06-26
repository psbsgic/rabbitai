import { t, ChartMetadata, ChartPlugin } from '@rabbitai-ui/core';
import transformProps from './transformProps';
import thumbnail from './images/thumbnail.png';
import controlPanel from './controlPanel';

const metadata = new ChartMetadata({
  name: t('Filter box'),
  description:
    'A multi filter, multi-choice filter box to make dashboards interactive',
  thumbnail,
  useLegacyApi: true,
});

export default class FilterBoxChartPlugin extends ChartPlugin {
  constructor() {
    super({
      controlPanel,
      metadata,
      transformProps,
      loadChart: () => import('./FilterBox.jsx'),
    });
  }
}
