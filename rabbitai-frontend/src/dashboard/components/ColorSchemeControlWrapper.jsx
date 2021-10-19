/* eslint-env browser */
import PropTypes from 'prop-types';
import React from 'react';
import { getCategoricalSchemeRegistry, t } from '@superset-ui/core';

import ColorSchemeControl from 'src/explore/components/controls/ColorSchemeControl';

const propTypes = {
  onChange: PropTypes.func,
  labelMargin: PropTypes.number,
  colorScheme: PropTypes.string,
};

const defaultProps = {
  colorScheme: undefined,
  onChange: () => {},
};

class ColorSchemeControlWrapper extends React.PureComponent {
  constructor(props) {
    super(props);
    this.state = { hovered: false };
    this.categoricalSchemeRegistry = getCategoricalSchemeRegistry();
    this.choices = this.categoricalSchemeRegistry.keys().map(s => [s, s]);
    this.schemes = this.categoricalSchemeRegistry.getMap();
  }

  setHover(hovered) {
    this.setState({ hovered });
  }

  render() {
    const { colorScheme, labelMargin = 0 } = this.props;
    return (
      <ColorSchemeControl
        description={t(
          "Any color palette selected here will override the colors applied to this dashboard's individual charts",
        )}
        label={t('Color scheme')}
        labelMargin={labelMargin}
        name="color_scheme"
        onChange={this.props.onChange}
        value={colorScheme}
        choices={this.choices}
        clearable
        schemes={this.schemes}
        hovered={this.state.hovered}
      />
    );
  }
}

ColorSchemeControlWrapper.propTypes = propTypes;
ColorSchemeControlWrapper.defaultProps = defaultProps;

export default ColorSchemeControlWrapper;
