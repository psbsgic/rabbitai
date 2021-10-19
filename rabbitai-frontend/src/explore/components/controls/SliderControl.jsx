import React from 'react';
import PropTypes from 'prop-types';
import Slider from 'src/components/Slider';
import ControlHeader from 'src/explore/components/ControlHeader';

const propTypes = {
  onChange: PropTypes.func,
  value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
};

const defaultProps = {
  onChange: () => {},
};

export default function SliderControl(props) {
  return (
    <>
      <ControlHeader {...props} />
      <Slider {...props} defaultValue={props.default} />
    </>
  );
}

SliderControl.propTypes = propTypes;
SliderControl.defaultProps = defaultProps;
