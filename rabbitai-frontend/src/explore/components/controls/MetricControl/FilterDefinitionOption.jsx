import React from 'react';
import PropTypes from 'prop-types';

import columnType from './columnType';
import adhocMetricType from './adhocMetricType';
import { StyledColumnOption } from '../../optionRenderers';

const propTypes = {
  option: PropTypes.oneOfType([
    columnType,
    PropTypes.shape({ saved_metric_name: PropTypes.string.isRequired }),
    adhocMetricType,
  ]).isRequired,
};

export default function FilterDefinitionOption({ option }) {
  if (option.saved_metric_name) {
    return (
      <StyledColumnOption
        column={{ column_name: option.saved_metric_name, type: 'expression' }}
        showType
      />
    );
  }
  if (option.column_name) {
    return <StyledColumnOption column={option} showType />;
  }
  if (option.label) {
    return (
      <StyledColumnOption
        column={{ column_name: option.label, type: 'expression' }}
        showType
      />
    );
  }
  return null;
}
FilterDefinitionOption.propTypes = propTypes;
