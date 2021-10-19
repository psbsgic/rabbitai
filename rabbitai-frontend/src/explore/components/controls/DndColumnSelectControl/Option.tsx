import React, { useCallback } from 'react';
import { styled, t, useTheme } from '@superset-ui/core';
import Icons from 'src/components/Icons';
import {
  CaretContainer,
  CloseContainer,
  OptionControlContainer,
  Label,
} from 'src/explore/components/controls/OptionControls';
import { OptionProps } from 'src/explore/components/controls/DndColumnSelectControl/types';
import { InfoTooltipWithTrigger } from '@superset-ui/chart-controls';

const StyledInfoTooltipWithTrigger = styled(InfoTooltipWithTrigger)`
  margin: 0 ${({ theme }) => theme.gridUnit}px;
`;

export default function Option({
  children,
  index,
  clickClose,
  withCaret,
  isExtra,
  canDelete = true,
}: OptionProps) {
  const theme = useTheme();
  const onClickClose = useCallback(
    e => {
      e.stopPropagation();
      clickClose(index);
    },
    [clickClose, index],
  );
  return (
    <OptionControlContainer data-test="option-label" withCaret={withCaret}>
      {canDelete && (
        <CloseContainer
          role="button"
          data-test="remove-control-button"
          onClick={onClickClose}
        >
          <Icons.XSmall iconColor={theme.colors.grayscale.light1} />
        </CloseContainer>
      )}
      <Label data-test="control-label">{children}</Label>
      {isExtra && (
        <StyledInfoTooltipWithTrigger
          icon="exclamation-triangle"
          placement="top"
          bsStyle="warning"
          tooltip={t(`
                This filter was inherited from the dashboard's context.
                It won't be saved when saving the chart.
              `)}
        />
      )}
      {withCaret && (
        <CaretContainer>
          <Icons.CaretRight iconColor={theme.colors.grayscale.light1} />
        </CaretContainer>
      )}
    </OptionControlContainer>
  );
}
