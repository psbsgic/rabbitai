import React from 'react';
import { styled } from '@superset-ui/core';
import { Progress as AntdProgress } from 'antd';
import { ProgressProps } from 'antd/lib/progress/progress';

export interface ProgressBarProps extends ProgressProps {
  striped?: boolean;
}

// eslint-disable-next-line @typescript-eslint/no-unused-vars
const ProgressBar = styled(({ striped, ...props }: ProgressBarProps) => (
  <AntdProgress {...props} />
))`
  line-height: 0;
  position: static;
  .ant-progress-inner {
    position: static;
  }
  .ant-progress-outer {
    ${({ percent }) => !percent && `display: none;`}
  }
  .ant-progress-text {
    font-size: ${({ theme }) => theme.typography.sizes.s}px;
  }
  .ant-progress-bg {
    position: static;
    ${({ striped }) =>
      striped &&
      `
        background-image: linear-gradient(45deg,
            rgba(255, 255, 255, 0.15) 25%,
            transparent 25%, transparent 50%,
            rgba(255, 255, 255, 0.15) 50%,
            rgba(255, 255, 255, 0.15) 75%,
            transparent 75%, transparent) !important;
        background-size: 1rem 1rem !important;
        `};
  }
`;

export default ProgressBar;
