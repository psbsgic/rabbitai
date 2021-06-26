
import React from 'react';
import { HTML5Backend } from 'react-dnd-html5-backend';
import { DndProvider } from 'react-dnd';
import { render, screen, waitFor } from 'spec/helpers/testing-library';
import userEvent from '@testing-library/user-event';
import DatasourcePanel, {
  Props as DatasourcePanelProps,
} from 'src/explore/components/DatasourcePanel';
import { columns, metrics } from 'spec/javascripts/datasource/fixtures';
import { DatasourceType } from '@rabbitai-ui/core/lib/query/types/Datasource';
import DatasourceControl from 'src/explore/components/controls/DatasourceControl';

const datasource = {
  id: 1,
  type: DatasourceType.Table,
  name: 'birth_names',
  columns,
  metrics,
  uid: '1__table',
  database: {
    backend: 'mysql',
    name: 'main',
  },
  column_format: { ratio: '.2%' },
  verbose_map: { __timestamp: 'Time' },
  main_dttm_col: 'None',
  datasource_name: 'table1',
  description: 'desc',
};
const props = {
  datasource,
  controls: {
    datasource: {
      validationErrors: null,
      mapStateToProps: () => ({ value: undefined }),
      type: DatasourceControl,
      label: 'hello',
      datasource,
    },
  },
  actions: {
    setControlValue: () => ({
      type: 'type',
      controlName: 'control',
      value: 'val',
      validationErrors: [],
    }),
  },
};

const setup = (props: DatasourcePanelProps) => (
  <DndProvider backend={HTML5Backend}>
    <DatasourcePanel {...props} />
  </DndProvider>
);

function search(value: string, input: HTMLElement) {
  userEvent.clear(input);
  userEvent.type(input, value);
}

test('should render', () => {
  const { container } = render(setup(props));
  expect(container).toBeVisible();
});

test('should display items in controls', () => {
  render(setup(props));
  expect(screen.getByText('birth_names')).toBeInTheDocument();
  expect(screen.getByText('Metrics')).toBeInTheDocument();
  expect(screen.getByText('Columns')).toBeInTheDocument();
});

test('should render the metrics', () => {
  render(setup(props));
  const metricsNum = metrics.length;
  metrics.forEach(metric =>
    expect(screen.getByText(metric.metric_name)).toBeInTheDocument(),
  );
  expect(
    screen.getByText(`Showing ${metricsNum} of ${metricsNum}`),
  ).toBeInTheDocument();
});

test('should render the columns', () => {
  render(setup(props));
  const columnsNum = columns.length;
  columns.forEach(col =>
    expect(screen.getByText(col.column_name)).toBeInTheDocument(),
  );
  expect(
    screen.getByText(`Showing ${columnsNum} of ${columnsNum}`),
  ).toBeInTheDocument();
});

test('should render 0 search results', async () => {
  render(setup(props));
  const searchInput = screen.getByPlaceholderText('Search Metrics & Columns');

  search('nothing', searchInput);
  expect(await screen.findByText('Showing 0 of 0')).toBeInTheDocument();
});

test('should search and render matching columns', async () => {
  render(setup(props));
  const searchInput = screen.getByPlaceholderText('Search Metrics & Columns');

  search(columns[0].column_name, searchInput);

  await waitFor(() => {
    expect(screen.getByText(columns[0].column_name)).toBeInTheDocument();
    expect(screen.queryByText(columns[1].column_name)).not.toBeInTheDocument();
  });
});

test('should search and render matching metrics', async () => {
  render(setup(props));
  const searchInput = screen.getByPlaceholderText('Search Metrics & Columns');

  search(metrics[0].metric_name, searchInput);

  await waitFor(() => {
    expect(screen.getByText(metrics[0].metric_name)).toBeInTheDocument();
    expect(screen.queryByText(metrics[1].metric_name)).not.toBeInTheDocument();
  });
});

test('should render a warning', async () => {
  const deprecatedDatasource = {
    ...datasource,
    extra: JSON.stringify({ warning_markdown: 'This is a warning.' }),
  };
  render(
    setup({
      ...props,
      datasource: deprecatedDatasource,
      controls: {
        datasource: {
          ...props.controls.datasource,
          datasource: deprecatedDatasource,
        },
      },
    }),
  );
  expect(
    await screen.findByRole('img', { name: 'alert-solid' }),
  ).toBeInTheDocument();
});
