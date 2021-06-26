
import { styled } from '@rabbitai-ui/core';

export const ExplorePopoverContent = styled.div`
  .edit-popover-resize {
    transform: scaleX(-1);
    float: right;
    margin-top: ${({ theme }) => theme.gridUnit * 4}px;
    margin-right: ${({ theme }) => theme.gridUnit * -2}px;
    cursor: nwse-resize;
  }
  .filter-sql-editor {
    border: ${({ theme }) => theme.colors.grayscale.light2} solid thin;
  }
  .custom-sql-disabled-message {
    color: ${({ theme }) => theme.colors.grayscale.light1};
    font-size: ${({ theme }) => theme.typography.sizes.xs}px;
    text-align: center;
    margin-top: ${({ theme }) => theme.gridUnit * 15}px;
  }
`;
