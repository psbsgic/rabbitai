import React, { useMemo, useRef } from 'react';
import {
  useDrag,
  useDrop,
  DropTargetMonitor,
  DragSourceMonitor,
} from 'react-dnd';
import { DragContainer } from 'src/explore/components/controls/OptionControls';
import {
  OptionProps,
  OptionItemInterface,
} from 'src/explore/components/controls/DndColumnSelectControl/types';
import Option from './Option';

export default function OptionWrapper(
  props: OptionProps & {
    type: string;
    onShiftOptions: (dragIndex: number, hoverIndex: number) => void;
  },
) {
  const {
    index,
    type,
    onShiftOptions,
    clickClose,
    withCaret,
    isExtra,
    canDelete = true,
    children,
    ...rest
  } = props;
  const ref = useRef<HTMLDivElement>(null);

  const item: OptionItemInterface = useMemo(
    () => ({
      dragIndex: index,
      type,
    }),
    [index, type],
  );
  const [, drag] = useDrag({
    item,
    collect: (monitor: DragSourceMonitor) => ({
      isDragging: monitor.isDragging(),
    }),
  });

  const [, drop] = useDrop({
    accept: type,

    hover: (item: OptionItemInterface, monitor: DropTargetMonitor) => {
      if (!ref.current) {
        return;
      }
      const { dragIndex } = item;
      const hoverIndex = index;

      // Don't replace items with themselves
      if (dragIndex === hoverIndex) {
        return;
      }
      // Determine rectangle on screen
      const hoverBoundingRect = ref.current?.getBoundingClientRect();
      // Get vertical middle
      const hoverMiddleY =
        (hoverBoundingRect.bottom - hoverBoundingRect.top) / 2;
      // Determine mouse position
      const clientOffset = monitor.getClientOffset();
      // Get pixels to the top
      const hoverClientY = clientOffset?.y
        ? clientOffset?.y - hoverBoundingRect.top
        : 0;
      // Only perform the move when the mouse has crossed half of the items height
      // When dragging downwards, only move when the cursor is below 50%
      // When dragging upwards, only move when the cursor is above 50%
      // Dragging downwards
      if (dragIndex < hoverIndex && hoverClientY < hoverMiddleY) {
        return;
      }
      // Dragging upwards
      if (dragIndex > hoverIndex && hoverClientY > hoverMiddleY) {
        return;
      }

      // Time to actually perform the action
      onShiftOptions(dragIndex, hoverIndex);
      // eslint-disable-next-line no-param-reassign
      item.dragIndex = hoverIndex;
    },
  });

  drag(drop(ref));

  return (
    <DragContainer ref={ref} {...rest}>
      <Option
        index={index}
        clickClose={clickClose}
        withCaret={withCaret}
        isExtra={isExtra}
        canDelete={canDelete}
      >
        {children}
      </Option>
    </DragContainer>
  );
}
