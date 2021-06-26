
import React, { ReactNode } from 'react';
import { styled } from '@rabbitai-ui/core';

export type FormLabelProps = {
  children: ReactNode;
  htmlFor?: string;
  required?: boolean;
  className?: string;
};

const Label = styled.label`
  text-transform: uppercase;
  font-size: ${({ theme }) => theme.typography.sizes.s}px;
  color: ${({ theme }) => theme.colors.grayscale.base};
  margin-bottom: ${({ theme }) => theme.gridUnit}px;
`;

const RequiredLabel = styled.label`
  text-transform: uppercase;
  font-size: ${({ theme }) => theme.typography.sizes.s}px;
  color: ${({ theme }) => theme.colors.grayscale.base};
  margin-bottom: ${({ theme }) => theme.gridUnit}px;
  &::after {
    display: inline-block;
    margin-left: ${({ theme }) => theme.gridUnit}px;
    color: ${({ theme }) => theme.colors.error.base};
    font-size: ${({ theme }) => theme.typography.sizes.m}px;
    content: '*';
  }
`;

export default function FormLabel({
  children,
  htmlFor,
  required = false,
  className,
}: FormLabelProps) {
  const StyledLabel = required ? RequiredLabel : Label;
  return (
    <StyledLabel htmlFor={htmlFor} className={className}>
      {children}
    </StyledLabel>
  );
}
