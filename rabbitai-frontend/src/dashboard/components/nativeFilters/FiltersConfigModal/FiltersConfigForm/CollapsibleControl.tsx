
import React, { ReactNode, useState } from 'react';
import { styled } from '@rabbitai-ui/core';
import { Checkbox } from 'src/common/components';

interface CollapsibleControlProps {
  checked?: boolean;
  title: string;
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
  const { checked = false, title, children, onChange } = props;
  const [isChecked, setIsChecked] = useState(checked);
  return (
    <StyledContainer checked={isChecked}>
      <Checkbox
        className="checkbox"
        checked={isChecked}
        onChange={e => {
          const value = e.target.checked;
          setIsChecked(value);
          if (onChange) {
            onChange(value);
          }
        }}
      >
        {title}
      </Checkbox>
      {isChecked && children}
    </StyledContainer>
  );
};

export { CollapsibleControl, CollapsibleControlProps };
