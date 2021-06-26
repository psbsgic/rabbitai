
import React from 'react';
import { useTheme } from '@rabbitai-ui/core';
import Icons from 'src/components/Icons';
import {
  CaretContainer,
  CloseContainer,
  OptionControlContainer,
  Label,
} from 'src/explore/components/controls/OptionControls';
import { OptionProps } from 'src/explore/components/controls/DndColumnSelectControl/types';

export default function Option(props: OptionProps) {
  const theme = useTheme();
  return (
    <OptionControlContainer
      data-test="option-label"
      withCaret={props.withCaret}
    >
      <CloseContainer
        role="button"
        data-test="remove-control-button"
        onClick={() => props.clickClose(props.index)}
      >
        <Icons.XSmall iconColor={theme.colors.grayscale.light1} />
      </CloseContainer>
      <Label data-test="control-label">{props.children}</Label>
      {props.withCaret && (
        <CaretContainer>
          <Icons.CaretRight iconColor={theme.colors.grayscale.light1} />
        </CaretContainer>
      )}
    </OptionControlContainer>
  );
}
