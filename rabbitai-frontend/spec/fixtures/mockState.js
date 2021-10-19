import datasources from 'spec/fixtures/mockDatasource';
import messageToasts from 'spec/javascripts/messageToasts/mockMessageToasts';
import {
  nativeFiltersInfo,
  mockDataMaskInfo,
} from 'spec/javascripts/dashboard/fixtures/mockNativeFilters';
import chartQueries from './mockChartQueries';
import { dashboardLayout } from './mockDashboardLayout';
import dashboardInfo from './mockDashboardInfo';
import { emptyFilters } from './mockDashboardFilters';
import dashboardState from './mockDashboardState';
import { sliceEntitiesForChart } from './mockSliceEntities';
import { user } from '../javascripts/sqllab/fixtures';

export default {
  datasources,
  sliceEntities: sliceEntitiesForChart,
  charts: chartQueries,
  nativeFilters: nativeFiltersInfo,
  dataMask: mockDataMaskInfo,
  dashboardInfo,
  dashboardFilters: emptyFilters,
  dashboardState,
  dashboardLayout,
  messageToasts,
  user,
  impressionId: 'mock_impression_id',
};
