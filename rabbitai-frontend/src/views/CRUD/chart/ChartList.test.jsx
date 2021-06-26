
import React from 'react';
import thunk from 'redux-thunk';
import configureStore from 'redux-mock-store';
import { Provider } from 'react-redux';
import fetchMock from 'fetch-mock';
import * as featureFlags from 'src/featureFlags';
import waitForComponentToPaint from 'spec/helpers/waitForComponentToPaint';
import { styledMount as mount } from 'spec/helpers/theming';
import { render, screen, cleanup } from 'spec/helpers/testing-library';
import userEvent from '@testing-library/user-event';
import { QueryParamProvider } from 'use-query-params';
import { act } from 'react-dom/test-utils';

import ChartList from 'src/views/CRUD/chart/ChartList';
import ConfirmStatusChange from 'src/components/ConfirmStatusChange';
import ListView from 'src/components/ListView';
import PropertiesModal from 'src/explore/components/PropertiesModal';
import ListViewCard from 'src/components/ListViewCard';
// store needed for withToasts(ChartTable)
const mockStore = configureStore([thunk]);
const store = mockStore({});

const chartsInfoEndpoint = 'glob:*/api/v1/chart/_info*';
const chartssOwnersEndpoint = 'glob:*/api/v1/chart/related/owners*';
const chartsCreatedByEndpoint = 'glob:*/api/v1/chart/related/created_by*';
const chartsEndpoint = 'glob:*/api/v1/chart/*';
const chartsVizTypesEndpoint = 'glob:*/api/v1/chart/viz_types';
const chartsDatasourcesEndpoint = 'glob:*/api/v1/chart/datasources';
const chartFavoriteStatusEndpoint = 'glob:*/api/v1/chart/favorite_status*';
const datasetEndpoint = 'glob:*/api/v1/dataset/*';

const mockCharts = [...new Array(3)].map((_, i) => ({
  changed_on: new Date().toISOString(),
  creator: 'super user',
  id: i,
  slice_name: `cool chart ${i}`,
  url: 'url',
  viz_type: 'bar',
  datasource_name: `ds${i}`,
  thumbnail_url: '/thumbnail',
}));

const mockUser = {
  userId: 1,
};

fetchMock.get(chartsInfoEndpoint, {
  permissions: ['can_read', 'can_write'],
});

fetchMock.get(chartssOwnersEndpoint, {
  result: [],
});
fetchMock.get(chartsCreatedByEndpoint, {
  result: [],
});
fetchMock.get(chartFavoriteStatusEndpoint, {
  result: [],
});
fetchMock.get(chartsEndpoint, {
  result: mockCharts,
  chart_count: 3,
});

fetchMock.get(chartsVizTypesEndpoint, {
  result: [],
  count: 0,
});

fetchMock.get(chartsDatasourcesEndpoint, {
  result: [],
  count: 0,
});

fetchMock.get(datasetEndpoint, {});

global.URL.createObjectURL = jest.fn();
fetchMock.get('/thumbnail', { body: new Blob(), sendAsJson: false });

describe('ChartList', () => {
  const isFeatureEnabledMock = jest
    .spyOn(featureFlags, 'isFeatureEnabled')
    .mockImplementation(feature => feature === 'LISTVIEWS_DEFAULT_CARD_VIEW');

  afterAll(() => {
    isFeatureEnabledMock.restore();
  });
  const mockedProps = {};

  const wrapper = mount(
    <Provider store={store}>
      <ChartList {...mockedProps} user={mockUser} />
    </Provider>,
  );

  beforeAll(async () => {
    await waitForComponentToPaint(wrapper);
  });

  it('renders', () => {
    expect(wrapper.find(ChartList)).toExist();
  });

  it('renders a ListView', () => {
    expect(wrapper.find(ListView)).toExist();
  });

  it('fetches info', () => {
    const callsI = fetchMock.calls(/chart\/_info/);
    expect(callsI).toHaveLength(1);
  });

  it('fetches data', () => {
    wrapper.update();
    const callsD = fetchMock.calls(/chart\/\?q/);
    expect(callsD).toHaveLength(1);
    expect(callsD[0][0]).toMatchInlineSnapshot(
      `"http://localhost/api/v1/chart/?q=(order_column:changed_on_delta_humanized,order_direction:desc,page:0,page_size:25)"`,
    );
  });

  it('renders a card view', () => {
    expect(wrapper.find(ListViewCard)).toExist();
  });

  it('renders a table view', async () => {
    wrapper.find('[data-test="list-view"]').first().simulate('click');
    await waitForComponentToPaint(wrapper);
    expect(wrapper.find('table')).toExist();
  });

  it('edits', async () => {
    expect(wrapper.find(PropertiesModal)).not.toExist();
    wrapper.find('[data-test="edit-alt"]').first().simulate('click');
    await waitForComponentToPaint(wrapper);
    expect(wrapper.find(PropertiesModal)).toExist();
  });

  it('delete', async () => {
    wrapper.find('[data-test="trash"]').first().simulate('click');
    await waitForComponentToPaint(wrapper);
    expect(wrapper.find(ConfirmStatusChange)).toExist();
  });
});

describe('RTL', () => {
  async function renderAndWait() {
    const mounted = act(async () => {
      const mockedProps = {};
      render(
        <QueryParamProvider>
          <ChartList {...mockedProps} user={mockUser} />
        </QueryParamProvider>,
        { useRedux: true },
      );
    });

    return mounted;
  }

  let isFeatureEnabledMock;
  beforeEach(async () => {
    isFeatureEnabledMock = jest
      .spyOn(featureFlags, 'isFeatureEnabled')
      .mockImplementation(() => true);
    await renderAndWait();
  });

  afterEach(() => {
    cleanup();
    isFeatureEnabledMock.mockRestore();
  });

  it('renders an "Import Chart" tooltip under import button', async () => {
    const importButton = screen.getByTestId('import-button');
    userEvent.hover(importButton);

    await screen.findByRole('tooltip');
    const importTooltip = screen.getByRole('tooltip', {
      name: 'Import charts',
    });

    expect(importTooltip).toBeInTheDocument();
  });
});