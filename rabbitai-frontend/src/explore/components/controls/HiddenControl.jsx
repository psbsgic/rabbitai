
import React from 'react';
import PropTypes from 'prop-types';
import { Input } from 'src/common/components';

const propTypes = {
  onChange: PropTypes.func,
  value: PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.number,
    PropTypes.object,
    PropTypes.bool,
    PropTypes.array,
    PropTypes.func,
  ]),
};

const defaultProps = {
  onChange: () => {},
};

export default function HiddenControl(props) {
  // This wouldn't be necessary but might as well
  return <Input type="hidden" value={props.value} />;
}

HiddenControl.propTypes = propTypes;
HiddenControl.defaultProps = defaultProps;
