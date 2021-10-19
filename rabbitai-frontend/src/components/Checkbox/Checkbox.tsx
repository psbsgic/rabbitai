import React from 'react';
import { styled } from '@superset-ui/core';
import { CheckboxChecked, CheckboxUnchecked } from 'src/components/Checkbox';

interface CheckboxProps {
  checked: boolean;
  onChange: (val?: boolean) => void;
  style?: React.CSSProperties;
}

const Styles = styled.span`
  &,
  & svg {
    vertical-align: top;
  }
`;

export default function Checkbox({ checked, onChange, style }: CheckboxProps) {
  return (
    <Styles
      style={style}
      onClick={() => {
        onChange(!checked);
      }}
      role="checkbox"
      tabIndex={0}
      aria-checked={checked}
      aria-label="Checkbox"
    >
      {checked ? <CheckboxChecked /> : <CheckboxUnchecked />}
    </Styles>
  );
}
