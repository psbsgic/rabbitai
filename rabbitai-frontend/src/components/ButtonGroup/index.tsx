import React from 'react';

export interface ButtonGroupProps {
  className?: string;
  children: React.ReactNode;
}

export default function ButtonGroup(props: ButtonGroupProps) {
  const { className, children } = props;
  return (
    <div
      role="group"
      className={className}
      css={{
        '& :nth-child(1):not(:nth-last-child(1))': {
          borderTopRightRadius: 0,
          borderBottomRightRadius: 0,
          borderRight: 0,
          marginLeft: 0,
        },
        '& :not(:nth-child(1)):not(:nth-last-child(1))': {
          borderRadius: 0,
          borderRight: 0,
          marginLeft: 0,
        },
        '& :nth-last-child(1):not(:nth-child(1))': {
          borderTopLeftRadius: 0,
          borderBottomLeftRadius: 0,
          marginLeft: 0,
        },
      }}
    >
      {children}
    </div>
  );
}
