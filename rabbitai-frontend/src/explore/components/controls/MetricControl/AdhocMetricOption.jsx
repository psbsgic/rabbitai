import React from 'react';
import PropTypes from 'prop-types';
import { OptionControlLabel } from 'src/explore/components/controls/OptionControls';
import { DndItemType } from 'src/explore/components/DndItemType';
import columnType from './columnType';
import AdhocMetric from './AdhocMetric';
import savedMetricType from './savedMetricType';
import AdhocMetricPopoverTrigger from './AdhocMetricPopoverTrigger';

const propTypes = {
  adhocMetric: PropTypes.instanceOf(AdhocMetric),
  onMetricEdit: PropTypes.func.isRequired,
  onRemoveMetric: PropTypes.func,
  columns: PropTypes.arrayOf(columnType),
  savedMetricsOptions: PropTypes.arrayOf(savedMetricType),
  savedMetric: savedMetricType,
  datasourceType: PropTypes.string,
  onMoveLabel: PropTypes.func,
  onDropLabel: PropTypes.func,
  index: PropTypes.number,
  type: PropTypes.string,
  multi: PropTypes.bool,
};

class AdhocMetricOption extends React.PureComponent {
  constructor(props) {
    super(props);
    this.onRemoveMetric = this.onRemoveMetric.bind(this);
  }

  onRemoveMetric(e) {
    e.stopPropagation();
    this.props.onRemoveMetric(this.props.index);
  }

  render() {
    const {
      adhocMetric,
      onMetricEdit,
      columns,
      savedMetricsOptions,
      savedMetric,
      datasourceType,
      onMoveLabel,
      onDropLabel,
      index,
      type,
      multi,
    } = this.props;

    return (
      <AdhocMetricPopoverTrigger
        adhocMetric={adhocMetric}
        onMetricEdit={onMetricEdit}
        columns={columns}
        savedMetricsOptions={savedMetricsOptions}
        savedMetric={savedMetric}
        datasourceType={datasourceType}
      >
        <OptionControlLabel
          savedMetric={savedMetric}
          adhocMetric={adhocMetric}
          label={adhocMetric.label}
          onRemove={this.onRemoveMetric}
          onMoveLabel={onMoveLabel}
          onDropLabel={onDropLabel}
          index={index}
          type={type ?? DndItemType.AdhocMetricOption}
          withCaret
          isFunction
          multi={multi}
        />
      </AdhocMetricPopoverTrigger>
    );
  }
}

export default AdhocMetricOption;

AdhocMetricOption.propTypes = propTypes;
