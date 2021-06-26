
import userEvent from '@testing-library/user-event';
import React from 'react';
import { render, screen } from 'spec/helpers/testing-library';
import { Indicator } from 'src/dashboard/components/FiltersBadge/selectors';
import DetailsPanel from '.';

const createProps = () => ({
  appliedCrossFilterIndicators: [
    {
      column: 'clinical_stage',
      name: 'Clinical Stage',
      value: [],
      status: 'UNSET',
      path: [
        'ROOT_ID',
        'TABS-wUKya7eQ0Z',
        'TAB-BCIJF4NvgQ',
        'ROW-xSeNAspgw',
        'CHART-eirDduqb1A',
      ],
    },
  ] as Indicator[],
  appliedIndicators: [
    {
      column: 'country_name',
      name: 'Country',
      value: [],
      status: 'UNSET',
      path: [
        'ROOT_ID',
        'TABS-wUKya7eQ0Z',
        'TAB-BCIJF4NvgQ',
        'ROW-xSeNAspgw',
        'CHART-eirDduqb1A',
      ],
    },
  ] as Indicator[],
  incompatibleIndicators: [
    {
      column: 'product_category_copy',
      name: 'Vaccine Approach Copy',
      value: [],
      status: 'UNSET',
      path: [
        'ROOT_ID',
        'TABS-wUKya7eQ0Zz',
        'TAB-BCIJF4NvgQq',
        'ROW-xSeNAspgww',
        'CHART-eirDduqb1Aa',
      ],
    },
  ] as Indicator[],
  unsetIndicators: [
    {
      column: 'product_category',
      name: 'Vaccine Approach',
      value: [],
      status: 'UNSET',
      path: [
        'ROOT_ID',
        'TABS-wUKya7eQ0Z',
        'TAB-BCIJF4NvgQ',
        'ROW-xSeNAspgw',
        'CHART-eirDduqb1A',
      ],
    },
  ] as Indicator[],
  onHighlightFilterSource: jest.fn(),
});

test('Should render "appliedCrossFilterIndicators"', () => {
  const props = createProps();
  props.appliedIndicators = [];
  props.incompatibleIndicators = [];
  props.unsetIndicators = [];

  render(
    <DetailsPanel {...props}>
      <div data-test="details-panel-content">Content</div>
    </DetailsPanel>,
  );

  userEvent.click(screen.getByTestId('details-panel-content'));
  expect(screen.getByText('Applied Cross Filters (1)')).toBeInTheDocument();
  expect(
    screen.getByRole('button', { name: 'search Clinical Stage' }),
  ).toBeInTheDocument();

  expect(props.onHighlightFilterSource).toBeCalledTimes(0);
  userEvent.click(
    screen.getByRole('button', { name: 'search Clinical Stage' }),
  );
  expect(props.onHighlightFilterSource).toBeCalledTimes(1);
  expect(props.onHighlightFilterSource).toBeCalledWith([
    'ROOT_ID',
    'TABS-wUKya7eQ0Z',
    'TAB-BCIJF4NvgQ',
    'ROW-xSeNAspgw',
    'CHART-eirDduqb1A',
    'LABEL-clinical_stage',
  ]);
});

test('Should render "appliedIndicators"', () => {
  const props = createProps();
  props.appliedCrossFilterIndicators = [];
  props.incompatibleIndicators = [];
  props.unsetIndicators = [];

  render(
    <DetailsPanel {...props}>
      <div data-test="details-panel-content">Content</div>
    </DetailsPanel>,
  );

  userEvent.click(screen.getByTestId('details-panel-content'));
  expect(screen.getByText('Applied Filters (1)')).toBeInTheDocument();
  expect(
    screen.getByRole('button', { name: 'search Country' }),
  ).toBeInTheDocument();

  expect(props.onHighlightFilterSource).toBeCalledTimes(0);
  userEvent.click(screen.getByRole('button', { name: 'search Country' }));
  expect(props.onHighlightFilterSource).toBeCalledTimes(1);
  expect(props.onHighlightFilterSource).toBeCalledWith([
    'ROOT_ID',
    'TABS-wUKya7eQ0Z',
    'TAB-BCIJF4NvgQ',
    'ROW-xSeNAspgw',
    'CHART-eirDduqb1A',
    'LABEL-country_name',
  ]);
});

test('Should render "incompatibleIndicators"', () => {
  const props = createProps();
  props.appliedCrossFilterIndicators = [];
  props.appliedIndicators = [];
  props.unsetIndicators = [];

  render(
    <DetailsPanel {...props}>
      <div data-test="details-panel-content">Content</div>
    </DetailsPanel>,
  );

  userEvent.click(screen.getByTestId('details-panel-content'));
  expect(screen.getByText('Incompatible Filters (1)')).toBeInTheDocument();
  expect(
    screen.getByRole('button', { name: 'search Vaccine Approach Copy' }),
  ).toBeInTheDocument();

  expect(props.onHighlightFilterSource).toBeCalledTimes(0);
  userEvent.click(
    screen.getByRole('button', { name: 'search Vaccine Approach Copy' }),
  );
  expect(props.onHighlightFilterSource).toBeCalledTimes(1);
  expect(props.onHighlightFilterSource).toBeCalledWith([
    'ROOT_ID',
    'TABS-wUKya7eQ0Zz',
    'TAB-BCIJF4NvgQq',
    'ROW-xSeNAspgww',
    'CHART-eirDduqb1Aa',
    'LABEL-product_category_copy',
  ]);
});

test('Should render "unsetIndicators"', () => {
  const props = createProps();
  props.appliedCrossFilterIndicators = [];
  props.appliedIndicators = [];
  props.incompatibleIndicators = [];

  render(
    <DetailsPanel {...props}>
      <div data-test="details-panel-content">Content</div>
    </DetailsPanel>,
  );

  userEvent.click(screen.getByTestId('details-panel-content'));
  expect(screen.getByText('Unset Filters (1)')).toBeInTheDocument();
  expect(
    screen.getByRole('button', { name: 'search Vaccine Approach' }),
  ).toBeInTheDocument();

  expect(props.onHighlightFilterSource).toBeCalledTimes(0);
  userEvent.click(
    screen.getByRole('button', { name: 'search Vaccine Approach' }),
  );
  expect(props.onHighlightFilterSource).toBeCalledTimes(1);
  expect(props.onHighlightFilterSource).toBeCalledWith([
    'ROOT_ID',
    'TABS-wUKya7eQ0Z',
    'TAB-BCIJF4NvgQ',
    'ROW-xSeNAspgw',
    'CHART-eirDduqb1A',
    'LABEL-product_category',
  ]);
});

test('Should render empty', () => {
  const props = createProps();
  props.appliedCrossFilterIndicators = [];
  props.appliedIndicators = [];
  props.incompatibleIndicators = [];
  props.unsetIndicators = [];

  render(
    <DetailsPanel {...props}>
      <div data-test="details-panel-content">Content</div>
    </DetailsPanel>,
  );

  expect(screen.getByTestId('details-panel-content')).toBeInTheDocument();
  userEvent.click(screen.getByTestId('details-panel-content'));
  expect(screen.queryByRole('button')).not.toBeInTheDocument();
});
