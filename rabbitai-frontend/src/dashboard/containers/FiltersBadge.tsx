
import { connect } from 'react-redux';
import { bindActionCreators, Dispatch } from 'redux';
import { uniqWith } from 'lodash';
import { setDirectPathToChild } from 'src/dashboard/actions/dashboardState';
import {
  selectIndicatorsForChart,
  Indicator,
  IndicatorStatus,
  selectNativeIndicatorsForChart,
} from 'src/dashboard/components/FiltersBadge/selectors';
import FiltersBadge from 'src/dashboard/components/FiltersBadge';

export interface FiltersBadgeProps {
  chartId: number;
}

const mapDispatchToProps = (dispatch: Dispatch) =>
  bindActionCreators(
    {
      onHighlightFilterSource: setDirectPathToChild,
    },
    dispatch,
  );

const sortByStatus = (indicators: Indicator[]): Indicator[] => {
  const statuses = [
    IndicatorStatus.Applied,
    IndicatorStatus.Unset,
    IndicatorStatus.Incompatible,
  ];
  return indicators.sort(
    (a, b) =>
      statuses.indexOf(a.status as IndicatorStatus) -
      statuses.indexOf(b.status as IndicatorStatus),
  );
};

const mapStateToProps = (
  {
    datasources,
    dashboardFilters,
    nativeFilters,
    dashboardInfo,
    charts,
    dataMask,
    dashboardLayout: { present },
  }: any,
  { chartId }: FiltersBadgeProps,
) => {
  const dashboardIndicators = selectIndicatorsForChart(
    chartId,
    dashboardFilters,
    datasources,
    charts,
  );

  const nativeIndicators = selectNativeIndicatorsForChart(
    nativeFilters,
    dataMask,
    chartId,
    charts,
    present,
    dashboardInfo.metadata?.chart_configuration,
  );

  const indicators = uniqWith(
    sortByStatus([...dashboardIndicators, ...nativeIndicators]),
    (ind1, ind2) =>
      ind1.column === ind2.column &&
      ind1.name === ind2.name &&
      (ind1.status !== IndicatorStatus.Applied ||
        ind2.status !== IndicatorStatus.Applied),
  );

  const appliedCrossFilterIndicators = indicators.filter(
    indicator => indicator.status === IndicatorStatus.CrossFilterApplied,
  );
  const appliedIndicators = indicators.filter(
    indicator => indicator.status === IndicatorStatus.Applied,
  );
  const unsetIndicators = indicators.filter(
    indicator => indicator.status === IndicatorStatus.Unset,
  );
  const incompatibleIndicators = indicators.filter(
    indicator => indicator.status === IndicatorStatus.Incompatible,
  );

  return {
    chartId,
    appliedIndicators,
    appliedCrossFilterIndicators,
    unsetIndicators,
    incompatibleIndicators,
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(FiltersBadge);
