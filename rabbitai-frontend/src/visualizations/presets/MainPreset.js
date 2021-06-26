import { isFeatureEnabled, Preset } from '@rabbitai-ui/core';
import {
  BigNumberChartPlugin,
  BigNumberTotalChartPlugin,
} from '@rabbitai-ui/legacy-preset-chart-big-number';
import CalendarChartPlugin from '@rabbitai-ui/legacy-plugin-chart-calendar';
import ChordChartPlugin from '@rabbitai-ui/legacy-plugin-chart-chord';
import CountryMapChartPlugin from '@rabbitai-ui/legacy-plugin-chart-country-map';
import EventFlowChartPlugin from '@rabbitai-ui/legacy-plugin-chart-event-flow';
import HeatmapChartPlugin from '@rabbitai-ui/legacy-plugin-chart-heatmap';
import HistogramChartPlugin from '@rabbitai-ui/legacy-plugin-chart-histogram';
import HorizonChartPlugin from '@rabbitai-ui/legacy-plugin-chart-horizon';
import MapBoxChartPlugin from '@rabbitai-ui/legacy-plugin-chart-map-box';
import PairedTTestChartPlugin from '@rabbitai-ui/legacy-plugin-chart-paired-t-test';
import ParallelCoordinatesChartPlugin from '@rabbitai-ui/legacy-plugin-chart-parallel-coordinates';
import PartitionChartPlugin from '@rabbitai-ui/legacy-plugin-chart-partition';
import PivotTableChartPlugin from '@rabbitai-ui/legacy-plugin-chart-pivot-table';
import RoseChartPlugin from '@rabbitai-ui/legacy-plugin-chart-rose';
import SankeyChartPlugin from '@rabbitai-ui/legacy-plugin-chart-sankey';
import SunburstChartPlugin from '@rabbitai-ui/legacy-plugin-chart-sunburst';
import TableChartPlugin from '@rabbitai-ui/plugin-chart-table';
import TreemapChartPlugin from '@rabbitai-ui/legacy-plugin-chart-treemap';
import { WordCloudChartPlugin } from '@rabbitai-ui/plugin-chart-word-cloud';
import WorldMapChartPlugin from '@rabbitai-ui/legacy-plugin-chart-world-map';
import {
  AreaChartPlugin,
  BarChartPlugin,
  BubbleChartPlugin,
  BulletChartPlugin,
  CompareChartPlugin,
  DistBarChartPlugin,
  DualLineChartPlugin,
  LineChartPlugin,
  LineMultiChartPlugin,
  TimePivotChartPlugin,
} from '@rabbitai-ui/legacy-preset-chart-nvd3';
import { DeckGLChartPreset } from '@rabbitai-ui/legacy-preset-chart-deckgl';
import {
  EchartsPieChartPlugin,
  EchartsBoxPlotChartPlugin,
  EchartsTimeseriesChartPlugin,
  EchartsGraphChartPlugin,
  EchartsGaugeChartPlugin,
  EchartsRadarChartPlugin,
  EchartsFunnelChartPlugin,
  EchartsTreemapChartPlugin,
  EchartsMixedTimeseriesChartPlugin,
  EchartsTreeChartPlugin,
} from '@rabbitai-ui/plugin-chart-echarts';
import {
  SelectFilterPlugin,
  RangeFilterPlugin,
  TimeFilterPlugin,
  TimeColumnFilterPlugin,
  TimeGrainFilterPlugin,
  GroupByFilterPlugin,
} from 'src/filters/components/';
import { PivotTableChartPlugin as PivotTableChartPluginV2 } from '@rabbitai-ui/plugin-chart-pivot-table';
import FilterBoxChartPlugin from '../FilterBox/FilterBoxChartPlugin';
import TimeTableChartPlugin from '../TimeTable/TimeTableChartPlugin';
import { FeatureFlag } from '../../featureFlags';

export default class MainPreset extends Preset {
  constructor() {
    const experimentalplugins = isFeatureEnabled(
      FeatureFlag.DASHBOARD_FILTERS_EXPERIMENTAL,
    )
      ? [new GroupByFilterPlugin().configure({ key: 'filter_groupby' })]
      : [];

    super({
      name: 'Legacy charts',
      presets: [new DeckGLChartPreset()],
      plugins: [
        new AreaChartPlugin().configure({ key: 'area' }),
        new BarChartPlugin().configure({ key: 'bar' }),
        new BigNumberChartPlugin().configure({ key: 'big_number' }),
        new BigNumberTotalChartPlugin().configure({ key: 'big_number_total' }),
        new EchartsBoxPlotChartPlugin().configure({ key: 'box_plot' }),
        new BubbleChartPlugin().configure({ key: 'bubble' }),
        new BulletChartPlugin().configure({ key: 'bullet' }),
        new CalendarChartPlugin().configure({ key: 'cal_heatmap' }),
        new ChordChartPlugin().configure({ key: 'chord' }),
        new CompareChartPlugin().configure({ key: 'compare' }),
        new CountryMapChartPlugin().configure({ key: 'country_map' }),
        new DistBarChartPlugin().configure({ key: 'dist_bar' }),
        new DualLineChartPlugin().configure({ key: 'dual_line' }),
        new EventFlowChartPlugin().configure({ key: 'event_flow' }),
        new FilterBoxChartPlugin().configure({ key: 'filter_box' }),
        new EchartsFunnelChartPlugin().configure({ key: 'funnel' }),
        new EchartsTreemapChartPlugin().configure({ key: 'treemap_v2' }),
        new EchartsGaugeChartPlugin().configure({ key: 'gauge_chart' }),
        new EchartsGraphChartPlugin().configure({ key: 'graph_chart' }),
        new EchartsRadarChartPlugin().configure({ key: 'radar' }),
        new EchartsMixedTimeseriesChartPlugin().configure({
          key: 'mixed_timeseries',
        }),
        new HeatmapChartPlugin().configure({ key: 'heatmap' }),
        new HistogramChartPlugin().configure({ key: 'histogram' }),
        new HorizonChartPlugin().configure({ key: 'horizon' }),
        new LineChartPlugin().configure({ key: 'line' }),
        new LineMultiChartPlugin().configure({ key: 'line_multi' }),
        new MapBoxChartPlugin().configure({ key: 'mapbox' }),
        new PairedTTestChartPlugin().configure({ key: 'paired_ttest' }),
        new ParallelCoordinatesChartPlugin().configure({ key: 'para' }),
        new PartitionChartPlugin().configure({ key: 'partition' }),
        new EchartsPieChartPlugin().configure({ key: 'pie' }),
        new PivotTableChartPlugin().configure({ key: 'pivot_table' }),
        new PivotTableChartPluginV2().configure({ key: 'pivot_table_v2' }),
        new RoseChartPlugin().configure({ key: 'rose' }),
        new SankeyChartPlugin().configure({ key: 'sankey' }),
        new SunburstChartPlugin().configure({ key: 'sunburst' }),
        new TableChartPlugin().configure({ key: 'table' }),
        new TimePivotChartPlugin().configure({ key: 'time_pivot' }),
        new TimeTableChartPlugin().configure({ key: 'time_table' }),
        new TreemapChartPlugin().configure({ key: 'treemap' }),
        new WordCloudChartPlugin().configure({ key: 'word_cloud' }),
        new WorldMapChartPlugin().configure({ key: 'world_map' }),
        new EchartsTimeseriesChartPlugin().configure({
          key: 'echarts_timeseries',
        }),
        new SelectFilterPlugin().configure({ key: 'filter_select' }),
        new RangeFilterPlugin().configure({ key: 'filter_range' }),
        new TimeFilterPlugin().configure({ key: 'filter_time' }),
        new TimeColumnFilterPlugin().configure({ key: 'filter_timecolumn' }),
        new TimeGrainFilterPlugin().configure({ key: 'filter_timegrain' }),
        new EchartsTreeChartPlugin().configure({ key: 'tree_chart' }),
        ...experimentalplugins,
      ],
    });
  }
}
