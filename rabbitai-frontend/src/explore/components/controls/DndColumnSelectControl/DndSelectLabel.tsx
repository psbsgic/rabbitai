import React from 'react';
import { useDrop } from 'react-dnd';
import { t, useTheme } from '@superset-ui/core';
import ControlHeader from 'src/explore/components/ControlHeader';
import {
  AddControlLabel,
  DndLabelsContainer,
  HeaderContainer,
} from 'src/explore/components/controls/OptionControls';
import { DatasourcePanelDndItem } from 'src/explore/components/DatasourcePanel/types';
import Icons from 'src/components/Icons';
import { DndColumnSelectProps } from './types';

export default function DndSelectLabel<T, O>({
  displayGhostButton = true,
  ...props
}: DndColumnSelectProps<T, O>) {
  const theme = useTheme();

  const [{ isOver, canDrop }, datasourcePanelDrop] = useDrop({
    accept: props.accept,

    drop: (item: DatasourcePanelDndItem) => {
      props.onDrop(item);
    },

    canDrop: (item: DatasourcePanelDndItem) => props.canDrop(item),

    collect: monitor => ({
      isOver: monitor.isOver(),
      canDrop: monitor.canDrop(),
      type: monitor.getItemType(),
    }),
  });

  function renderGhostButton() {
    return (
      <AddControlLabel cancelHover>
        <Icons.PlusSmall iconColor={theme.colors.grayscale.light1} />
        {t(props.ghostButtonText || 'Drop columns here')}
      </AddControlLabel>
    );
  }

  return (
    <div ref={datasourcePanelDrop}>
      <HeaderContainer>
        <ControlHeader {...props} />
      </HeaderContainer>
      <DndLabelsContainer canDrop={canDrop} isOver={isOver}>
        {props.valuesRenderer()}
        {displayGhostButton && renderGhostButton()}
      </DndLabelsContainer>
    </div>
  );
}
