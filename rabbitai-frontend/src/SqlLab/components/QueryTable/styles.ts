import { styled, css } from '@superset-ui/core';
import { IconTooltip } from '../../../components/IconTooltip';

export const StaticPosition = css`
  position: static;
`;

export const verticalAlign = css`
  vertical-align: 0em;
  svg {
    height: 0.9em;
  }
`;

export const StyledTooltip = styled(IconTooltip)`
  padding-right: ${({ theme }) => theme.gridUnit * 2}px;
  span {
    color: ${({ theme }) => theme.colors.grayscale.base};
    &: hover {
      color: ${({ theme }) => theme.colors.primary.base};
    }
  }
`;
