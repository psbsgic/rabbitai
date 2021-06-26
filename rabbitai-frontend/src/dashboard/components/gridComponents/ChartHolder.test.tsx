

import React from 'react';
import { render, screen } from 'spec/helpers/testing-library';
import mockState from 'spec/fixtures/mockState';
import { sliceId as chartId } from 'spec/fixtures/mockChartQueries';
import newComponentFactory from 'src/dashboard/util/newComponentFactory';
import userEvent from '@testing-library/user-event';
import { waitFor } from '@testing-library/react';
import { ChartHolder } from './index';
import { CHART_TYPE, ROW_TYPE } from '../../util/componentTypes';

describe('ChartHolder', () => {
  const defaultProps = {
    component: {
      ...newComponentFactory(CHART_TYPE),
      id: 'CHART_ID',
      parents: ['ROOT_ID', 'TABS_ID', 'TAB_ID', 'ROW_ID'],
      meta: {
        chartId,
        width: 3,
        height: 10,
        chartName: 'Mock chart name',
      },
    },
    parentComponent: {
      ...newComponentFactory(ROW_TYPE),
      id: 'ROW_ID',
      children: ['COLUMN_ID'],
    },
    index: 0,
    depth: 0,
    id: 'CHART_ID',
    parentId: 'ROW_ID',
    availableColumnCount: 12,
    columnWidth: 300,
    onResizeStart: () => {},
    onResize: () => {},
    onResizeStop: () => {},
    handleComponentDrop: () => {},
    deleteComponent: () => {},
    updateComponents: () => {},
    editMode: false,
    isComponentVisible: true,
    dashboardId: 123,
  };

  const renderWrapper = (props = defaultProps, state = mockState) =>
    render(<ChartHolder {...props} />, {
      useRedux: true,
      initialState: state,
      useDnd: true,
    });

  it('toggle full size', async () => {
    renderWrapper();

    let chart = (screen.getByTestId('slice-container')
      .firstChild as HTMLElement).style;
    expect(chart?.width).toBe('900px');
    expect(chart?.height).toBe('26px');

    userEvent.click(screen.getByRole('button'));
    userEvent.click(screen.getByText('Maximize chart'));

    chart = (screen.getByTestId('slice-container').firstChild as HTMLElement)
      .style;
    await waitFor(() => expect(chart?.width).toBe('992px'));
    expect(chart?.height).toBe('714px');
  });
});
