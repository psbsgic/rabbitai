
import React from 'react';
import PropTypes from 'prop-types';
import adhocMetricType from 'src/explore/components/controls/MetricControl/adhocMetricType';
import { OptionControlLabel } from 'src/explore/components/controls/OptionControls';
import { DndItemType } from 'src/explore/components/DndItemType';
import columnType from 'src/explore/components/controls/FilterControl/columnType';
import AdhocFilterPopoverTrigger from 'src/explore/components/controls/FilterControl/AdhocFilterPopoverTrigger';
import AdhocFilter from 'src/explore/components/controls/FilterControl/AdhocFilter';

const propTypes = {
  adhocFilter: PropTypes.instanceOf(AdhocFilter).isRequired,
  onFilterEdit: PropTypes.func.isRequired,
  onRemoveFilter: PropTypes.func,
  options: PropTypes.arrayOf(
    PropTypes.oneOfType([
      columnType,
      PropTypes.shape({ saved_metric_name: PropTypes.string.isRequired }),
      adhocMetricType,
    ]),
  ).isRequired,
  datasource: PropTypes.object,
  partitionColumn: PropTypes.string,
  onMoveLabel: PropTypes.func,
  onDropLabel: PropTypes.func,
  index: PropTypes.number,
};

const AdhocFilterOption = ({
  adhocFilter,
  options,
  datasource,
  onFilterEdit,
  onRemoveFilter,
  partitionColumn,
  onMoveLabel,
  onDropLabel,
  index,
}) => (
  <AdhocFilterPopoverTrigger
    adhocFilter={adhocFilter}
    options={options}
    datasource={datasource}
    onFilterEdit={onFilterEdit}
    partitionColumn={partitionColumn}
  >
    <OptionControlLabel
      label={adhocFilter.getDefaultLabel()}
      tooltipTitle={adhocFilter.getTooltipTitle()}
      onRemove={onRemoveFilter}
      onMoveLabel={onMoveLabel}
      onDropLabel={onDropLabel}
      index={index}
      type={DndItemType.FilterOption}
      withCaret
      isExtra={adhocFilter.isExtra}
    />
  </AdhocFilterPopoverTrigger>
);

export default AdhocFilterOption;

AdhocFilterOption.propTypes = propTypes;
