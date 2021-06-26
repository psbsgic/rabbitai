
import React from 'react';
import { styledMount as mount } from 'spec/helpers/theming';
import { act } from 'react-dom/test-utils';
import { ReactWrapper } from 'enzyme';
import { Provider } from 'react-redux';
import fetchMock from 'fetch-mock';
import thunk from 'redux-thunk';
import waitForComponentToPaint from 'spec/helpers/waitForComponentToPaint';
import configureStore from 'redux-mock-store';
import ActivityTable from 'src/views/CRUD/welcome/ActivityTable';

const mockStore = configureStore([thunk]);
const store = mockStore({});

const chartsEndpoint = 'glob:*/api/v1/chart/?*';
const dashboardsEndpoint = 'glob:*/api/v1/dashboard/?*';

const mockData = {
  Viewed: [
    {
      slice_name: 'ChartyChart',
      changed_on_utc: '24 Feb 2014 10:13:14',
      url: '/fakeUrl/explore',
      id: '4',
      table: {},
    },
  ],
  Created: [
    {
      dashboard_title: 'Dashboard_Test',
      changed_on_utc: '24 Feb 2014 10:13:14',
      url: '/fakeUrl/dashboard',
      id: '3',
    },
  ],
};

fetchMock.get(chartsEndpoint, {
  result: [
    {
      slice_name: 'ChartyChart',
      changed_on_utc: '24 Feb 2014 10:13:14',
      url: '/fakeUrl/explore',
      id: '4',
      table: {},
    },
  ],
});

fetchMock.get(dashboardsEndpoint, {
  result: [
    {
      dashboard_title: 'Dashboard_Test',
      changed_on_utc: '24 Feb 2014 10:13:14',
      url: '/fakeUrl/dashboard',
      id: '3',
    },
  ],
});

describe('ActivityTable', () => {
  const activityProps = {
    activeChild: 'Created',
    activityData: mockData,
    setActiveChild: jest.fn(),
    user: { userId: '1' },
    loading: false,
  };

  let wrapper: ReactWrapper;

  beforeAll(async () => {
    await act(async () => {
      wrapper = mount(
        <Provider store={store}>
          <ActivityTable {...activityProps} />
        </Provider>,
      );
    });
  });

  it('the component renders', () => {
    expect(wrapper.find(ActivityTable)).toExist();
  });
  it('renders tabs with three buttons', () => {
    expect(wrapper.find('li.no-router')).toHaveLength(3);
  });
  it('renders ActivityCards', async () => {
    expect(wrapper.find('ListViewCard')).toExist();
  });
  it('calls the getEdited batch call when edited tab is clicked', async () => {
    act(() => {
      const handler = wrapper.find('li.no-router a').at(1).prop('onClick');
      if (handler) {
        handler({} as any);
      }
    });
    await waitForComponentToPaint(wrapper);
    const dashboardCall = fetchMock.calls(/dashboard\/\?q/);
    const chartCall = fetchMock.calls(/chart\/\?q/);
    expect(chartCall).toHaveLength(1);
    expect(dashboardCall).toHaveLength(1);
  });
  it('show empty state if there is no data', () => {
    const activityProps = {
      activeChild: 'Created',
      activityData: {},
      setActiveChild: jest.fn(),
      user: { userId: '1' },
      loading: false,
    };
    const wrapper = mount(
      <Provider store={store}>
        <ActivityTable {...activityProps} />
      </Provider>,
    );
    expect(wrapper.find('EmptyState')).toExist();
  });
});
