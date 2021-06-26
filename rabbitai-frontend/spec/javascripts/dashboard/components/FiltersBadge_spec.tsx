
import React from 'react';
import { shallow } from 'enzyme';
import { rabbitaiTheme } from '@rabbitai-ui/core';
import { Provider } from 'react-redux';
import * as RabbitaiUI from '@rabbitai-ui/core';
import { CHART_UPDATE_SUCCEEDED } from 'src/chart/chartAction';
import { buildActiveFilters } from 'src/dashboard/util/activeDashboardFilters';
import FiltersBadge from 'src/dashboard/containers/FiltersBadge';
import {
  getMockStoreWithFilters,
  getMockStoreWithNativeFilters,
} from 'spec/fixtures/mockStore';
import { sliceId } from 'spec/fixtures/mockChartQueries';
import { dashboardFilters } from 'spec/fixtures/mockDashboardFilters';
import { dashboardWithFilter } from 'spec/fixtures/mockDashboardLayout';
import Icons from 'src/components/Icons';
import { FeatureFlag } from 'src/featureFlags';

describe('FiltersBadge', () => {
  // there's this bizarre "active filters" thing
  // that doesn't actually use any kind of state management.
  // Have to set variables in there.
  buildActiveFilters({
    dashboardFilters,
    components: dashboardWithFilter,
  });

  beforeEach(() => {
    // shallow rendering in enzyme doesn't propagate contexts correctly,
    // so we have to mock the hook.
    // See https://medium.com/7shifts-engineering-blog/testing-usecontext-react-hook-with-enzyme-shallow-da062140fc83
    jest.spyOn(RabbitaiUI, 'useTheme').mockImplementation(() => rabbitaiTheme);
  });

  describe('for dashboard filters', () => {
    it("doesn't show number when there are no active filters", () => {
      const store = getMockStoreWithFilters();
      // start with basic dashboard state, dispatch an event to simulate query completion
      store.dispatch({
        type: CHART_UPDATE_SUCCEEDED,
        key: sliceId,
        queriesResponse: [
          {
            status: 'success',
            applied_filters: [],
            rejected_filters: [],
          },
        ],
        dashboardFilters,
      });
      const wrapper = shallow(
        <Provider store={store}>
          <FiltersBadge chartId={sliceId} />,
        </Provider>,
      );
      expect(
        wrapper.dive().find('[data-test="applied-filter-count"]'),
      ).not.toExist();
    });

    it('shows the indicator when filters have been applied', () => {
      const store = getMockStoreWithFilters();
      // start with basic dashboard state, dispatch an event to simulate query completion
      store.dispatch({
        type: CHART_UPDATE_SUCCEEDED,
        key: sliceId,
        queriesResponse: [
          {
            status: 'success',
            applied_filters: [{ column: 'region' }],
            rejected_filters: [],
          },
        ],
        dashboardFilters,
      });
      const wrapper = shallow(
        <FiltersBadge {...{ store }} chartId={sliceId} />,
      ).dive();
      expect(wrapper.dive().find('DetailsPanelPopover')).toExist();
      expect(
        wrapper.dive().find('[data-test="applied-filter-count"]'),
      ).toHaveText('1');
      expect(wrapper.dive().find('WarningFilled')).not.toExist();
    });

    it("shows a warning when there's a rejected filter", () => {
      const store = getMockStoreWithFilters();
      // start with basic dashboard state, dispatch an event to simulate query completion
      store.dispatch({
        type: CHART_UPDATE_SUCCEEDED,
        key: sliceId,
        queriesResponse: [
          {
            status: 'success',
            applied_filters: [],
            rejected_filters: [
              { column: 'region', reason: 'not_in_datasource' },
            ],
          },
        ],
        dashboardFilters,
      });
      const wrapper = shallow(
        <FiltersBadge {...{ store }} chartId={sliceId} />,
      ).dive();
      expect(wrapper.dive().find('DetailsPanelPopover')).toExist();
      expect(
        wrapper.dive().find('[data-test="applied-filter-count"]'),
      ).toHaveText('0');
      expect(
        wrapper.dive().find('[data-test="incompatible-filter-count"]'),
      ).toHaveText('1');
      // to look at the shape of the wrapper use:
      // console.log(wrapper.dive().debug())
      expect(wrapper.dive().find(Icons.AlertSolid)).toExist();
    });
  });

  describe('for native filters', () => {
    it("doesn't show number when there are no active filters", () => {
      const store = getMockStoreWithNativeFilters();
      // start with basic dashboard state, dispatch an event to simulate query completion
      store.dispatch({
        type: CHART_UPDATE_SUCCEEDED,
        key: sliceId,
        queriesResponse: [
          {
            status: 'success',
            applied_filters: [],
            rejected_filters: [],
          },
        ],
      });
      const wrapper = shallow(
        <Provider store={store}>
          <FiltersBadge chartId={sliceId} />,
        </Provider>,
      );
      expect(
        wrapper.dive().find('[data-test="applied-filter-count"]'),
      ).not.toExist();
    });

    it('shows the indicator when filters have been applied', () => {
      // @ts-ignore
      global.featureFlags = {
        [FeatureFlag.DASHBOARD_NATIVE_FILTERS]: true,
      };
      const store = getMockStoreWithNativeFilters();
      // start with basic dashboard state, dispatch an event to simulate query completion
      store.dispatch({
        type: CHART_UPDATE_SUCCEEDED,
        key: sliceId,
        queriesResponse: [
          {
            status: 'success',
            applied_filters: [{ column: 'region' }],
            rejected_filters: [],
          },
        ],
      });
      const wrapper = shallow(
        <FiltersBadge {...{ store }} chartId={sliceId} />,
      ).dive();
      expect(wrapper.dive().find('DetailsPanelPopover')).toExist();
      expect(
        wrapper.dive().find('[data-test="applied-filter-count"]'),
      ).toHaveText('1');
      expect(wrapper.dive().find('WarningFilled')).not.toExist();
    });

    it("shows a warning when there's a rejected filter", () => {
      // @ts-ignore
      global.featureFlags = {
        [FeatureFlag.DASHBOARD_NATIVE_FILTERS]: true,
      };
      const store = getMockStoreWithNativeFilters();
      // start with basic dashboard state, dispatch an event to simulate query completion
      store.dispatch({
        type: CHART_UPDATE_SUCCEEDED,
        key: sliceId,
        queriesResponse: [
          {
            status: 'success',
            applied_filters: [],
            rejected_filters: [
              { column: 'region', reason: 'not_in_datasource' },
            ],
          },
        ],
      });
      const wrapper = shallow(
        <FiltersBadge {...{ store }} chartId={sliceId} />,
      ).dive();
      expect(wrapper.dive().find('DetailsPanelPopover')).toExist();
      expect(
        wrapper.dive().find('[data-test="applied-filter-count"]'),
      ).toHaveText('0');
      expect(
        wrapper.dive().find('[data-test="incompatible-filter-count"]'),
      ).toHaveText('1');
      expect(wrapper.dive().find(Icons.AlertSolid)).toExist();
    });
  });
});
