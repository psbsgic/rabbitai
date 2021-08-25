import charts from 'src/chart/chartReducer';
import dataMask from 'src/dataMask/reducer';
import dashboardInfo from 'src/dashboard/reducers/dashboardInfo';
import dashboardState from 'src/dashboard/reducers/dashboardState';
import dashboardFilters from 'src/dashboard/reducers/dashboardFilters';
import nativeFilters from 'src/dashboard/reducers/nativeFilters';
import datasources from 'src/dashboard/reducers/datasources';
import sliceEntities from 'src/dashboard/reducers/sliceEntities';
import dashboardLayout from 'src/dashboard/reducers/undoableDashboardLayout';
import messageToasts from 'src/messageToasts/reducers';
import saveModal from 'src/explore/reducers/saveModalReducer';
import explore from 'src/explore/reducers/exploreReducer';
import sqlLab from 'src/SqlLab/reducers/sqlLab';
import localStorageUsageInKilobytes from 'src/SqlLab/reducers/localStorageUsage';

const impressionId = (state = '') => state;

const container = document.getElementById('app');
const bootstrap = JSON.parse(container?.getAttribute('data-bootstrap') ?? '{}');
const common = { ...bootstrap.common };

export default {
  charts,
  datasources,
  dashboardInfo,
  dashboardFilters,
  dataMask,
  nativeFilters,
  dashboardState,
  dashboardLayout,
  impressionId,
  messageToasts,
  sliceEntities,
  saveModal,
  explore,
  sqlLab,
  localStorageUsageInKilobytes,
  common: () => common,
};
