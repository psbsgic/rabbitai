import React from 'react';
import { t } from '@superset-ui/core';
import PropTypes from 'prop-types';
import { Input } from 'src/common/components';
import { Tooltip } from 'src/components/Tooltip';

const propTypes = {
  title: PropTypes.shape({
    label: PropTypes.string,
    hasCustomLabel: PropTypes.bool,
  }),
  onChange: PropTypes.func.isRequired,
  isEditDisabled: PropTypes.bool,
};

export default class AdhocMetricEditPopoverTitle extends React.Component {
  constructor(props) {
    super(props);
    this.onMouseOver = this.onMouseOver.bind(this);
    this.onMouseOut = this.onMouseOut.bind(this);
    this.onClick = this.onClick.bind(this);
    this.onBlur = this.onBlur.bind(this);
    this.onInputBlur = this.onInputBlur.bind(this);
    this.state = {
      isHovered: false,
      isEditMode: false,
    };
  }

  onMouseOver() {
    this.setState({ isHovered: true });
  }

  onMouseOut() {
    this.setState({ isHovered: false });
  }

  onClick() {
    this.setState({ isEditMode: true });
  }

  onBlur() {
    this.setState({ isEditMode: false });
  }

  onInputBlur(e) {
    if (e.target.value === '') {
      this.props.onChange(e);
    }
    this.onBlur();
  }

  render() {
    const { title, onChange, isEditDisabled } = this.props;
    const defaultLabel = t('My metric');

    if (isEditDisabled) {
      return (
        <span data-test="AdhocMetricTitle">{title.label || defaultLabel}</span>
      );
    }

    return this.state.isEditMode ? (
      <Input
        className="metric-edit-popover-label-input"
        type="text"
        placeholder={title.label}
        value={title.hasCustomLabel ? title.label : ''}
        autoFocus
        onChange={onChange}
        onBlur={this.onInputBlur}
        data-test="AdhocMetricEditTitle#input"
      />
    ) : (
      <Tooltip placement="top" title="Click to edit label">
        <span
          className="AdhocMetricEditPopoverTitle inline-editable"
          data-test="AdhocMetricEditTitle#trigger"
          onMouseOver={this.onMouseOver}
          onMouseOut={this.onMouseOut}
          onClick={this.onClick}
          onBlur={this.onBlur}
          role="button"
          tabIndex={0}
        >
          {title.label || defaultLabel}
          &nbsp;
          <i
            className="fa fa-pencil"
            style={{ color: this.state.isHovered ? 'black' : 'grey' }}
          />
        </span>
      </Tooltip>
    );
  }
}
AdhocMetricEditPopoverTitle.propTypes = propTypes;
