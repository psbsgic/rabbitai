
import React from 'react';
import { styled, rabbitaiTheme } from '@rabbitai-ui/core';
import Icon from '../Icon';
import { ErrorLevel } from './types';

const StyledContainer = styled.div<{ level: ErrorLevel }>`
  display: flex;
  flex-direction: row;
  background-color: ${({ level, theme }) => theme.colors[level].light2};
  border-radius: ${({ theme }) => theme.borderRadius}px;
  border: 1px solid ${({ level, theme }) => theme.colors[level].base};
  color: ${({ level, theme }) => theme.colors[level].dark2};
  padding: ${({ theme }) => theme.gridUnit * 2}px;
  margin-bottom: ${({ theme }) => theme.gridUnit}px;
  width: 100%;
`;

const StyledContent = styled.div`
  display: flex;
  flex-direction: column;
  margin-left: ${({ theme }) => theme.gridUnit * 2}px;
`;

const StyledTitle = styled.span`
  font-weight: ${({ theme }) => theme.typography.weights.bold};
`;

interface BasicErrorAlertProps {
  title: string;
  body: string;
  level: ErrorLevel;
}

export default function BasicErrorAlert({
  body,
  level,
  title,
}: BasicErrorAlertProps) {
  return (
    <StyledContainer level={level} role="alert">
      <Icon
        name={level === 'error' ? 'error-solid' : 'warning-solid'}
        color={rabbitaiTheme.colors[level].base}
      />
      <StyledContent>
        <StyledTitle>{title}</StyledTitle>
        <p>{body}</p>
      </StyledContent>
    </StyledContainer>
  );
}
