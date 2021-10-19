import React from 'react';
import PropTypes from 'prop-types';
import { InputNumber } from 'src/common/components';
import { t, styled } from '@superset-ui/core';
import { isEqual, debounce } from 'lodash';
import ControlHeader from 'src/explore/components/ControlHeader';

const propTypes = {
  onChange: PropTypes.func,
  value: PropTypes.array,
};

const defaultProps = {
  onChange: () => {},
  value: [null, null],
};

const StyledDiv = styled.div`
  display: flex;
`;

const MinInput = styled(InputNumber)`
  flex: 1;
  margin-right: ${({ theme }) => theme.gridUnit}px;
`;

const MaxInput = styled(InputNumber)`
  flex: 1;
  margin-left: ${({ theme }) => theme.gridUnit}px;
`;

export default class BoundsControl extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      minMax: [
        Number.isNaN(this.props.value[0]) ? '' : props.value[0],
        Number.isNaN(this.props.value[1]) ? '' : props.value[1],
      ],
    };
    this.onChange = debounce(this.onChange.bind(this), 300);
    this.onMinChange = this.onMinChange.bind(this);
    this.onMaxChange = this.onMaxChange.bind(this);
    this.update = this.update.bind(this);
  }

  componentDidUpdate(prevProps) {
    if (!isEqual(prevProps.value, this.props.value)) {
      this.update();
    }
  }

  update() {
    this.setState({
      minMax: [
        Number.isNaN(this.props.value[0]) ? '' : this.props.value[0],
        Number.isNaN(this.props.value[1]) ? '' : this.props.value[1],
      ],
    });
  }

  onMinChange(value) {
    this.setState(
      prevState => ({
        minMax: [value, prevState.minMax[1]],
      }),
      this.onChange,
    );
  }

  onMaxChange(value) {
    this.setState(
      prevState => ({
        minMax: [prevState.minMax[0], value],
      }),
      this.onChange,
    );
  }

  onChange() {
    const mm = this.state.minMax;
    const min = Number.isNaN(parseFloat(mm[0])) ? null : parseFloat(mm[0]);
    const max = Number.isNaN(parseFloat(mm[1])) ? null : parseFloat(mm[1]);
    this.props.onChange([min, max]);
  }

  render() {
    return (
      <div>
        <ControlHeader {...this.props} />
        <StyledDiv>
          <MinInput
            data-test="min-bound"
            placeholder={t('Min')}
            onChange={this.onMinChange}
            value={this.state.minMax[0]}
          />
          <MaxInput
            data-test="max-bound"
            placeholder={t('Max')}
            onChange={this.onMaxChange}
            value={this.state.minMax[1]}
          />
        </StyledDiv>
      </div>
    );
  }
}

BoundsControl.propTypes = propTypes;
BoundsControl.defaultProps = defaultProps;
