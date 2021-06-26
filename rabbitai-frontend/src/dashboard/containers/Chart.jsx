
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';

import {
  toggleExpandSlice,
  setFocusedFilterField,
  unsetFocusedFilterField,
} from '../actions/dashboardState';
import { updateComponents } from '../actions/dashboardLayout';
import { changeFilter } from '../actions/dashboardFilters';
import { addSuccessToast, addDangerToast } from '../../messageToasts/actions';
import { refreshChart } from '../../chart/chartAction';
import { logEvent } from '../../logger/actions';
import {
  getActiveFilters,
  getAppliedFilterValues,
} from '../util/activeDashboardFilters';
import getFormDataWithExtraFilters from '../util/charts/getFormDataWithExtraFilters';
import Chart from '../components/gridComponents/Chart';

const EMPTY_FILTERS = {};

function mapStateToProps(
  {
    charts: chartQueries,
    dashboardInfo,
    dashboardState,
    dashboardLayout,
    dataMask,
    datasources,
    sliceEntities,
    nativeFilters,
  },
  ownProps,
) {
  const { id } = ownProps;
  const chart = chartQueries[id] || {};
  const datasource =
    (chart && chart.form_data && datasources[chart.form_data.datasource]) || {};
  const { colorScheme, colorNamespace } = dashboardState;

  // note: this method caches filters if possible to prevent render cascades
  const formData = getFormDataWithExtraFilters({
    layout: dashboardLayout.present,
    chart,
    // eslint-disable-next-line camelcase
    chartConfiguration: dashboardInfo.metadata?.chart_configuration,
    charts: chartQueries,
    filters: getAppliedFilterValues(id),
    colorScheme,
    colorNamespace,
    sliceId: id,
    nativeFilters,
    dataMask,
  });

  formData.dashboardId = dashboardInfo.id;

  return {
    chart,
    datasource,
    slice: sliceEntities.slices[id],
    timeout: dashboardInfo.common.conf.RABBITAI_WEBSERVER_TIMEOUT,
    filters: getActiveFilters() || EMPTY_FILTERS,
    formData,
    editMode: dashboardState.editMode,
    isExpanded: !!dashboardState.expandedSlices[id],
    rabbitaiCanExplore: !!dashboardInfo.rabbitai_can_explore,
    rabbitaiCanShare: !!dashboardInfo.rabbitai_can_share,
    rabbitaiCanCSV: !!dashboardInfo.rabbitai_can_csv,
    sliceCanEdit: !!dashboardInfo.slice_can_edit,
    ownState: dataMask[id]?.ownState,
    filterState: dataMask[id]?.filterState,
  };
}

function mapDispatchToProps(dispatch) {
  return bindActionCreators(
    {
      updateComponents,
      addSuccessToast,
      addDangerToast,
      toggleExpandSlice,
      changeFilter,
      setFocusedFilterField,
      unsetFocusedFilterField,
      refreshChart,
      logEvent,
    },
    dispatch,
  );
}

export default connect(mapStateToProps, mapDispatchToProps)(Chart);
