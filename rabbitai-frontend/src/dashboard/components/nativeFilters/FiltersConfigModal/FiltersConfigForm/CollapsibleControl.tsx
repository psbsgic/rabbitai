import React, { ReactNode, useEffect, useState } from 'react';
import { styled } from '@superset-ui/core';
import { Checkbox } from 'src/common/components';
import { InfoTooltipWithTrigger } from '@superset-ui/chart-controls';

interface CollapsibleControlProps {
  initialValue?: boolean;
  disabled?: boolean;
  checked?: boolean;
  title: string;
  tooltip?: string;
  children: ReactNode;
  onChange?: (checked: boolean) => void;
}

const StyledContainer = styled.div<{ checked: boolean }>`
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  min-height: ${({ theme }) => theme.gridUnit * 10}px;
  padding-top: ${({ theme }) => theme.gridUnit * 2 + 2}px;

  .checkbox {
    margin-bottom: ${({ theme, checked }) => (checked ? theme.gridUnit : 0)}px;
  }

  & > div {
    margin-bottom: ${({ theme }) => theme.gridUnit * 2}px;
  }
`;

const CollapsibleControl = (props: CollapsibleControlProps) => {
  const {
    checked,
    disabled,
    title,
    tooltip,
    children,
    onChange = () => {},
    initialValue = false,
  } = props;
  const [isChecked, setIsChecked] = useState(initialValue);

  useEffect(() => {
    // if external `checked` changed to `undefined`, it means that we work now in uncontrolled mode with local state
    // and we need ignore external value
    if (checked !== undefined) {
      setIsChecked(checked);
    }
  }, [checked]);

  return (
    <StyledContainer checked={isChecked}>
      <Checkbox
        className="checkbox"
        checked={isChecked}
        disabled={disabled}
        onChange={e => {
          const value = e.target.checked;
          // external `checked` value has more priority then local state
          if (checked === undefined) {
            // uncontrolled mode
            setIsChecked(value);
          }
          onChange(value);
        }}
      >
        <>
          {title}&nbsp;
          {tooltip && (
            <InfoTooltipWithTrigger placement="top" tooltip={tooltip} />
          )}
        </>
      </Checkbox>
      {isChecked && children}
    </StyledContainer>
  );
};

export { CollapsibleControl, CollapsibleControlProps };
