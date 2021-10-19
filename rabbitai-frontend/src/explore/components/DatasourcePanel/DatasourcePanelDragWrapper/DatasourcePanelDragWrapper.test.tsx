import React from 'react';
import { DndProvider } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';
import { render, screen } from 'spec/helpers/testing-library';
import { DndItemType } from 'src/explore/components/DndItemType';
import DatasourcePanelDragWrapper from '.';

test('should render', () => {
  render(
    <DndProvider backend={HTML5Backend}>
      <DatasourcePanelDragWrapper
        value={{ metric_name: 'test' }}
        type={DndItemType.Metric}
      >
        <div data-test="children" />
      </DatasourcePanelDragWrapper>
    </DndProvider>,
  );

  expect(screen.getByTestId('DatasourcePanelDragWrapper')).toBeInTheDocument();
  expect(screen.getByTestId('children')).toBeInTheDocument();
});

test('should have attribute draggable:true', () => {
  render(
    <DndProvider backend={HTML5Backend}>
      <DatasourcePanelDragWrapper
        value={{ metric_name: 'test' }}
        type={DndItemType.Metric}
      >
        <div data-test="children" />
      </DatasourcePanelDragWrapper>
    </DndProvider>,
  );

  expect(screen.getByTestId('DatasourcePanelDragWrapper')).toHaveAttribute(
    'draggable',
    'true',
  );
});
