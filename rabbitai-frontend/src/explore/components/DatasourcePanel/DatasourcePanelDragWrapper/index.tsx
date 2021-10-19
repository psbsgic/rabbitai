import React, { ReactNode } from 'react';
import { useDrag } from 'react-dnd';
import { styled } from '@superset-ui/core';
import { DatasourcePanelDndItem } from '../types';

const DatasourceItemContainer = styled.div`
  display: flex;
  align-items: center;
  width: 100%;
  height: ${({ theme }) => theme.gridUnit * 6}px;
  cursor: pointer;

  > div {
    width: 100%;
  }

  :hover {
    background-color: ${({ theme }) => theme.colors.grayscale.light2};
  }
`;

interface DatasourcePanelDragWrapperProps extends DatasourcePanelDndItem {
  children?: ReactNode;
}

export default function DatasourcePanelDragWrapper(
  props: DatasourcePanelDragWrapperProps,
) {
  const [, drag] = useDrag({
    item: {
      value: props.value,
      type: props.type,
    },
  });

  return (
    <DatasourceItemContainer data-test="DatasourcePanelDragWrapper" ref={drag}>
      {props.children}
    </DatasourceItemContainer>
  );
}
