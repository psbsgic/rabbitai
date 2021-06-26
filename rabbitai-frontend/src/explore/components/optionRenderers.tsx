

import React from 'react';
import { styled } from '@rabbitai-ui/core';
import {
  MetricOption,
  ColumnOption,
  MetricOptionProps,
  ColumnOptionProps,
} from '@rabbitai-ui/chart-controls';

const OptionContainer = styled.div`
  > span {
    display: flex;
    align-items: center;
  }

  .option-label {
    display: inline-block;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    & ~ i {
      margin-left: ${({ theme }) => theme.gridUnit}px;
    }
  }
  .type-label {
    margin-right: ${({ theme }) => theme.gridUnit * 3}px;
    width: ${({ theme }) => theme.gridUnit * 7}px;
    display: inline-block;
    text-align: center;
    font-weight: ${({ theme }) => theme.typography.weights.bold};
  }
`;

export const StyledMetricOption = (props: MetricOptionProps) => (
  <OptionContainer>
    <MetricOption {...props} />
  </OptionContainer>
);

export const StyledColumnOption = (props: ColumnOptionProps) => (
  <OptionContainer>
    <ColumnOption {...props} />
  </OptionContainer>
);
