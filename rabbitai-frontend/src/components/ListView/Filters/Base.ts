import { ReactNode } from 'react';
import { styled } from '@superset-ui/core';

export interface BaseFilter {
  Header: ReactNode;
  initialValue: any;
}

export const FilterContainer = styled.div`
  display: inline-flex;
  margin-right: 2em;
  font-size: ${({ theme }) => theme.typography.sizes.s}px;
  align-items: center;
`;

export const FilterTitle = styled.label`
  font-weight: bold;
  margin: 0 0.4em 0 0;
`;
