import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';

import { updateDataMask } from 'src/dataMask/actions';
import DashboardHeader from '../components/Header';
import isDashboardLoading from '../util/isDashboardLoading';

import { dashboardInfoChanged } from '../actions/dashboardInfo';

import {
  setEditMode,
  showBuilderPane,
  fetchFaveStar,
  saveFaveStar,
  savePublished,
  setColorSchemeAndUnsavedChanges,
  fetchCharts,
  updateCss,
  onChange,
  saveDashboardRequest,
  setMaxUndoHistoryExceeded,
  maxUndoHistoryToast,
  setRefreshFrequency,
  onRefresh,
} from '../actions/dashboardState';

import {
  undoLayoutAction,
  redoLayoutAction,
  updateDashboardTitle,
  dashboardTitleChanged,
} from '../actions/dashboardLayout';

import {
  addSuccessToast,
  addDangerToast,
  addWarningToast,
} from '../../messageToasts/actions';

import { logEvent } from '../../logger/actions';
import { DASHBOARD_HEADER_ID } from '../util/constants';
import {
  fetchUISpecificReport,
  toggleActive,
  deleteActiveReport,
} from '../../reports/actions/reports';

function mapStateToProps({
  dashboardLayout: undoableLayout,
  dashboardState,
  reports,
  dashboardInfo,
  charts,
  dataMask,
  user,
}) {
  return {
    dashboardInfo,
    undoLength: undoableLayout.past.length,
    redoLength: undoableLayout.future.length,
    layout: undoableLayout.present,
    dashboardTitle: (
      (undoableLayout.present[DASHBOARD_HEADER_ID] || {}).meta || {}
    ).text,
    expandedSlices: dashboardState.expandedSlices,
    refreshFrequency: dashboardState.refreshFrequency,
    shouldPersistRefreshFrequency: !!dashboardState.shouldPersistRefreshFrequency,
    customCss: dashboardState.css,
    colorNamespace: dashboardState.colorNamespace,
    colorScheme: dashboardState.colorScheme,
    charts,
    dataMask,
    user,
    isStarred: !!dashboardState.isStarred,
    isPublished: !!dashboardState.isPublished,
    isLoading: isDashboardLoading(charts),
    hasUnsavedChanges: !!dashboardState.hasUnsavedChanges,
    maxUndoHistoryExceeded: !!dashboardState.maxUndoHistoryExceeded,
    lastModifiedTime: Math.max(
      dashboardState.lastModifiedTime,
      dashboardInfo.last_modified_time,
    ),
    editMode: !!dashboardState.editMode,
    slug: dashboardInfo.slug,
    metadata: dashboardInfo.metadata,
    reports,
  };
}

function mapDispatchToProps(dispatch) {
  return bindActionCreators(
    {
      addSuccessToast,
      addDangerToast,
      addWarningToast,
      onUndo: undoLayoutAction,
      onRedo: redoLayoutAction,
      setEditMode,
      showBuilderPane,
      setColorSchemeAndUnsavedChanges,
      fetchFaveStar,
      saveFaveStar,
      savePublished,
      fetchCharts,
      updateDashboardTitle,
      updateCss,
      onChange,
      onSave: saveDashboardRequest,
      setMaxUndoHistoryExceeded,
      maxUndoHistoryToast,
      logEvent,
      setRefreshFrequency,
      onRefresh,
      dashboardInfoChanged,
      dashboardTitleChanged,
      updateDataMask,
      fetchUISpecificReport,
      toggleActive,
      deleteActiveReport,
    },
    dispatch,
  );
}

export default connect(mapStateToProps, mapDispatchToProps)(DashboardHeader);
