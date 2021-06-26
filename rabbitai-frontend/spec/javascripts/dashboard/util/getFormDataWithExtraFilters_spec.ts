
import getFormDataWithExtraFilters, {
  GetFormDataWithExtraFiltersArguments,
} from 'src/dashboard/util/charts/getFormDataWithExtraFilters';
import { DASHBOARD_ROOT_ID } from 'src/dashboard/util/constants';
import { Filter } from 'src/dashboard/components/nativeFilters/types';
import { LayoutItem } from 'src/dashboard/types';
import { dashboardLayout } from '../../../fixtures/mockDashboardLayout';
import { sliceId as chartId } from '../../../fixtures/mockChartQueries';

describe('getFormDataWithExtraFilters', () => {
  const filterId = 'native-filter-1';
  const mockChart = {
    id: chartId,
    chartAlert: null,
    chartStatus: null,
    chartUpdateEndTime: null,
    chartUpdateStartTime: 1,
    lastRendered: 1,
    latestQueryFormData: {},
    sliceFormData: null,
    queryController: null,
    queriesResponse: null,
    triggerQuery: false,
    formData: {
      viz_type: 'filter_select',
      filters: [
        {
          col: 'country_name',
          op: 'IN',
          val: ['United States'],
        },
      ],
    },
  };
  const mockArgs: GetFormDataWithExtraFiltersArguments = {
    chartConfiguration: {},
    charts: {
      [chartId as number]: mockChart,
    },
    chart: mockChart,
    filters: {
      region: ['Spain'],
      color: ['pink', 'purple'],
    },
    sliceId: chartId,
    nativeFilters: {
      filterSets: {},
      filters: {
        [filterId]: ({
          id: filterId,
          scope: {
            rootPath: [DASHBOARD_ROOT_ID],
            excluded: [],
          },
        } as unknown) as Filter,
      },
    },
    dataMask: {
      [filterId]: {
        id: filterId,
        extraFormData: {},
        filterState: {},
        ownState: {},
      },
    },
    layout: (dashboardLayout.present as unknown) as {
      [key: string]: LayoutItem;
    },
  };

  it('should include filters from the passed filters', () => {
    const result = getFormDataWithExtraFilters(mockArgs);
    expect(result.extra_filters).toHaveLength(2);
    expect(result.extra_filters[0]).toEqual({
      col: 'region',
      op: 'IN',
      val: ['Spain'],
    });
    expect(result.extra_filters[1]).toEqual({
      col: 'color',
      op: 'IN',
      val: ['pink', 'purple'],
    });
  });
});
