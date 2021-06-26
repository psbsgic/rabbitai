
import React from 'react';
import { styled } from '@rabbitai-ui/core';
import { Tooltip } from 'src/components/Tooltip';
import { IconName } from 'src/components/Icon';
import Icons from 'src/components/Icons';
import { TooltipPlacement } from 'antd/lib/tooltip';

export type ActionProps = {
  label: string;
  tooltip?: string | React.ReactElement;
  placement?: TooltipPlacement;
  icon: IconName;
  onClick: () => void;
};

interface ActionsBarProps {
  actions: Array<ActionProps>;
}

const StyledActions = styled.span`
  white-space: nowrap;
  min-width: 100px;
  svg,
  i {
    margin-right: 8px;

    &:hover {
      path {
        fill: ${({ theme }) => theme.colors.primary.base};
      }
    }
  }
`;

const ActionWrapper = styled.span`
  color: ${({ theme }) => theme.colors.grayscale.base};
`;

export default function ActionsBar({ actions }: ActionsBarProps) {
  return (
    <StyledActions className="actions">
      {actions.map((action, index) => {
        const ActionIcon = Icons[action.icon];
        if (action.tooltip) {
          return (
            <Tooltip
              id={`${action.label}-tooltip`}
              title={action.tooltip}
              placement={action.placement}
              key={index}
            >
              <ActionWrapper
                role="button"
                tabIndex={0}
                className="action-button"
                data-test={action.label}
                onClick={action.onClick}
              >
                <ActionIcon />
              </ActionWrapper>
            </Tooltip>
          );
        }

        return (
          <ActionWrapper
            role="button"
            tabIndex={0}
            className="action-button"
            onClick={action.onClick}
            data-test={action.label}
            key={index}
          >
            <ActionIcon />
          </ActionWrapper>
        );
      })}
    </StyledActions>
  );
}
