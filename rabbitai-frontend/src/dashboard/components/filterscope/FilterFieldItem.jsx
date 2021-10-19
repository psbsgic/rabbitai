import React from 'react';
import PropTypes from 'prop-types';
import cx from 'classnames';
import { FormLabel } from 'src/components/Form';

const propTypes = {
  label: PropTypes.string.isRequired,
  isSelected: PropTypes.bool.isRequired,
};

export default function FilterFieldItem({ label, isSelected }) {
  return (
    <span
      className={cx('filter-field-item filter-container', {
        'is-selected': isSelected,
      })}
    >
      <FormLabel htmlFor={label}>{label}</FormLabel>
    </span>
  );
}

FilterFieldItem.propTypes = propTypes;
