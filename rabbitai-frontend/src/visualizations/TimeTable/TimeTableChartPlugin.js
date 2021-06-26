import { t, ChartMetadata, ChartPlugin } from '@rabbitai-ui/core';
import transformProps from './transformProps';
import thumbnail from './images/thumbnail.png';

const metadata = new ChartMetadata({
  name: t('Time-series Table'),
  description: '',
  thumbnail,
  useLegacyApi: true,
});

export default class TimeTableChartPlugin extends ChartPlugin {
  constructor() {
    super({
      metadata,
      transformProps,
      loadChart: () => import('./TimeTable.jsx'),
    });
  }
}
