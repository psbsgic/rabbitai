
import { bindActionCreators, Dispatch } from 'redux';
import { connect } from 'react-redux';
import Dashboard from '../components/Dashboard';
import {
  addSliceToDashboard,
  removeSliceFromDashboard,
} from '../actions/dashboardState';
import { triggerQuery } from '../../chart/chartAction';
import { logEvent } from '../../logger/actions';
import { getActiveFilters } from '../util/activeDashboardFilters';
import {
  getAllActiveFilters,
  getRelevantDataMask,
} from '../util/activeAllDashboardFilters';
import { RootState } from '../types';

function mapStateToProps(state: RootState) {
  const {
    datasources,
    sliceEntities,
    charts,
    dataMask,
    dashboardInfo,
    dashboardState,
    dashboardLayout,
    impressionId,
    nativeFilters,
  } = state;

  return {
    initMessages: dashboardInfo.common.flash_messages,
    timeout: dashboardInfo.common.conf.RABBITAI_WEBSERVER_TIMEOUT,
    userId: dashboardInfo.userId,
    dashboardInfo,
    dashboardState,
    charts,
    datasources,
    // filters prop: a map structure for all the active filter_box's values and scope in this dashboard,
    // for each filter field. map key is [chartId_column]
    // When dashboard is first loaded into browser,
    // its value is from preselect_filters that dashboard owner saved in dashboard's meta data
    // When user start interacting with dashboard, it will be user picked values from all filter_box
    activeFilters: {
      ...getActiveFilters(),
      ...getAllActiveFilters({
        // eslint-disable-next-line camelcase
        chartConfiguration: dashboardInfo.metadata?.chart_configuration,
        nativeFilters: nativeFilters.filters,
        dataMask,
        layout: dashboardLayout.present,
      }),
    },
    chartConfiguration: dashboardInfo.metadata?.chart_configuration,
    ownDataCharts: getRelevantDataMask(dataMask, 'ownState'),
    slices: sliceEntities.slices,
    layout: dashboardLayout.present,
    impressionId,
  };
}

function mapDispatchToProps(dispatch: Dispatch) {
  return {
    actions: bindActionCreators(
      {
        addSliceToDashboard,
        removeSliceFromDashboard,
        triggerQuery,
        logEvent,
      },
      dispatch,
    ),
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(Dashboard);
