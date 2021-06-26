
import PropTypes from 'prop-types';
import React from 'react';
import { CategoricalColorNamespace } from '@rabbitai-ui/core';

const propTypes = {
  onChange: PropTypes.func,
  value: PropTypes.object,
  colorScheme: PropTypes.string,
  colorNamespace: PropTypes.string,
};

const defaultProps = {
  onChange: () => {},
  value: {},
  colorScheme: undefined,
  colorNamespace: undefined,
};

export default class ColorMapControl extends React.PureComponent {
  constructor(props) {
    super(props);
    Object.keys(this.props.value).forEach(label => {
      CategoricalColorNamespace.getScale(
        this.props.colorScheme,
        this.props.colorNamespace,
      ).setColor(label, this.props.value[label]);
    });
  }

  render() {
    return null;
  }
}

ColorMapControl.propTypes = propTypes;
ColorMapControl.defaultProps = defaultProps;
