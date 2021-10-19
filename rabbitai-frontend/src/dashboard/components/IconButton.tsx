import React, { MouseEventHandler } from 'react';
import { styled } from '@superset-ui/core';

interface IconButtonProps {
  icon: JSX.Element;
  label?: string;
  onClick: MouseEventHandler<HTMLDivElement>;
}

const StyledDiv = styled.div`
  display: flex;
  align-items: center;
  color: ${({ theme }) => theme.colors.grayscale.base};
  &:hover {
    color: ${({ theme }) => theme.colors.primary.base};
  }
`;

const StyledSpan = styled.span`
  margin-left: ${({ theme }) => theme.gridUnit * 2}px;
`;

const IconButton = ({ icon, label, onClick }: IconButtonProps) => (
  <StyledDiv
    tabIndex={0}
    role="button"
    onClick={e => {
      e.preventDefault();
      onClick(e);
    }}
  >
    {icon}
    {label && <StyledSpan>{label}</StyledSpan>}
  </StyledDiv>
);

export default IconButton;
