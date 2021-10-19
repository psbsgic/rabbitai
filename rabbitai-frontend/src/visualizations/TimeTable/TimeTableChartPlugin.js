import { t, ChartMetadata, ChartPlugin } from '@superset-ui/core';
import transformProps from './transformProps';
import thumbnail from './images/thumbnail.png';

const metadata = new ChartMetadata({
  category: t('Table'),
  name: t('Time-series Table'),
  description: t(
    'Compare multiple time series charts (as sparklines) and related metrics quickly.',
  ),
  tags: [
    t('Multi-Variables'),
    t('Comparison'),
    t('Legacy'),
    t('Percentages'),
    t('Tabular'),
    t('Text'),
    t('Trend'),
  ],
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
