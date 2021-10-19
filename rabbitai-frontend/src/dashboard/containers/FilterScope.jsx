import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';

import { updateDashboardFiltersScope } from '../actions/dashboardFilters';
import { setUnsavedChanges } from '../actions/dashboardState';
import FilterScopeSelector from '../components/filterscope/FilterScopeSelector';

function mapStateToProps({ dashboardLayout, dashboardFilters }) {
  return {
    dashboardFilters,
    layout: dashboardLayout.present,
  };
}

function mapDispatchToProps(dispatch) {
  return bindActionCreators(
    {
      updateDashboardFiltersScope,
      setUnsavedChanges,
    },
    dispatch,
  );
}

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(FilterScopeSelector);
