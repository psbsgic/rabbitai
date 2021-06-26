
import React from 'react';
import PropTypes from 'prop-types';

import withToasts from 'src/messageToasts/enhancers/withToasts';
import {
  StyledColumnOption,
  StyledMetricOption,
} from 'src/explore/components/optionRenderers';
import AggregateOption from './AggregateOption';
import columnType from './columnType';
import aggregateOptionType from './aggregateOptionType';
import savedMetricType from './savedMetricType';

const propTypes = {
  option: PropTypes.oneOfType([
    columnType,
    savedMetricType,
    aggregateOptionType,
  ]).isRequired,
  addWarningToast: PropTypes.func.isRequired,
};

function MetricDefinitionOption({ option, addWarningToast }) {
  if (option.metric_name) {
    return <StyledMetricOption metric={option} showType />;
  }
  if (option.column_name) {
    return <StyledColumnOption column={option} showType />;
  }
  if (option.aggregate_name) {
    return <AggregateOption aggregate={option} showType />;
  }
  addWarningToast(
    'You must supply either a saved metric, column or aggregate to MetricDefinitionOption',
  );
  return null;
}

MetricDefinitionOption.propTypes = propTypes;

export default withToasts(MetricDefinitionOption);
