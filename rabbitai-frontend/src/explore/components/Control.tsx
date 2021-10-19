import React, { ReactNode, useCallback, useState } from 'react';
import { ControlType } from '@superset-ui/chart-controls';
import { JsonValue, QueryFormData } from '@superset-ui/core';
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

export default function Control(props: ControlProps) {
  const {
    actions: { setControlValue },
    name,
    type,
    hidden,
  } = props;

  const [hovered, setHovered] = useState(false);
  const onChange = useCallback(
    (value: any, errors: any[]) => setControlValue(name, value, errors),
    [name, setControlValue],
  );

  if (!type) return null;

  const ControlComponent = typeof type === 'string' ? controlMap[type] : type;
  if (!ControlComponent) {
    return <>Unknown controlType: {type}</>;
  }

  return (
    <div
      className="Control"
      data-test={name}
      style={hidden ? { display: 'none' } : undefined}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
    >
      <ErrorBoundary>
        <ControlComponent onChange={onChange} hovered={hovered} {...props} />
      </ErrorBoundary>
    </div>
  );
}
