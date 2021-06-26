
import React, { ReactNode } from 'react';
import { ControlType } from '@rabbitai-ui/chart-controls';
import { JsonValue, QueryFormData } from '@rabbitai-ui/core';
import ErrorBoundary from 'src/components/ErrorBoundary';
import { ExploreActions } from 'src/explore/actions/exploreActions';
import controlMap from './controls';

import './Control.less';

export type ControlProps = {
  // the actual action dispatcher (via bindActionCreators) has identical
  // signature to the original action factory.
  actions: Partial<ExploreActions> & Pick<ExploreActions, 'setControlValue'>;
  type: ControlType;
  label?: ReactNode;
  name: string;
  description?: ReactNode;
  tooltipOnClick?: () => ReactNode;
  places?: number;
  rightNode?: ReactNode;
  formData?: QueryFormData | null;
  value?: JsonValue;
  validationErrors?: any[];
  hidden?: boolean;
  renderTrigger?: boolean;
};

export default class Control extends React.PureComponent<
  ControlProps,
  { hovered: boolean }
> {
  onMouseEnter: () => void;

  onMouseLeave: () => void;

  constructor(props: ControlProps) {
    super(props);
    this.state = { hovered: false };
    this.onChange = this.onChange.bind(this);
    this.onMouseEnter = this.setHover.bind(this, true);
    this.onMouseLeave = this.setHover.bind(this, false);
  }

  onChange(value: any, errors: any[]) {
    this.props.actions.setControlValue(this.props.name, value, errors);
  }

  setHover(hovered: boolean) {
    this.setState({ hovered });
  }

  render() {
    const { type, hidden } = this.props;
    if (!type) return null;
    const ControlComponent = typeof type === 'string' ? controlMap[type] : type;
    if (!ControlComponent) {
      return `Unknown controlType: ${type}`;
    }
    return (
      <div
        className="Control"
        data-test={this.props.name}
        style={hidden ? { display: 'none' } : undefined}
        onMouseEnter={this.onMouseEnter}
        onMouseLeave={this.onMouseLeave}
      >
        <ErrorBoundary>
          <ControlComponent
            onChange={this.onChange}
            hovered={this.state.hovered}
            {...this.props}
          />
        </ErrorBoundary>
      </div>
    );
  }
}
