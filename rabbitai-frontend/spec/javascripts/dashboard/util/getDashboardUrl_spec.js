import getDashboardUrl from 'src/dashboard/util/getDashboardUrl';
import { DASHBOARD_FILTER_SCOPE_GLOBAL } from 'src/dashboard/reducers/dashboardFilters';
import { DashboardStandaloneMode } from '../../../../src/dashboard/util/constants';

describe('getChartIdsFromLayout', () => {
  const filters = {
    '35_key': {
      values: ['value'],
      scope: DASHBOARD_FILTER_SCOPE_GLOBAL,
    },
  };

  const globalLocation = window.location;
  afterEach(() => {
    window.location = globalLocation;
  });

  it('should encode filters', () => {
    const url = getDashboardUrl({ pathname: 'path', filters });
    expect(url).toBe(
      'path?preselect_filters=%7B%2235%22%3A%7B%22key%22%3A%5B%22value%22%5D%7D%7D',
    );
  });

  it('should encode filters with hash', () => {
    const urlWithHash = getDashboardUrl({
      pathname: 'path',
      filters,
      hash: 'iamhashtag',
    });
    expect(urlWithHash).toBe(
      'path?preselect_filters=%7B%2235%22%3A%7B%22key%22%3A%5B%22value%22%5D%7D%7D#iamhashtag',
    );
  });

  it('should encode filters with standalone', () => {
    const urlWithStandalone = getDashboardUrl({
      pathname: 'path',
      filters,
      standalone: DashboardStandaloneMode.HIDE_NAV,
    });
    expect(urlWithStandalone).toBe(
      `path?preselect_filters=%7B%2235%22%3A%7B%22key%22%3A%5B%22value%22%5D%7D%7D&standalone=${DashboardStandaloneMode.HIDE_NAV}`,
    );
  });

  it('should encode filters with missing standalone', () => {
    const urlWithStandalone = getDashboardUrl({
      pathname: 'path',
      filters,
      standalone: null,
    });
    expect(urlWithStandalone).toBe(
      'path?preselect_filters=%7B%2235%22%3A%7B%22key%22%3A%5B%22value%22%5D%7D%7D',
    );
  });

  it('should encode native filters', () => {
    const urlWithNativeFilters = getDashboardUrl({
      pathname: 'path',
      dataMask: {
        'NATIVE_FILTER-foo123': {
          filterState: {
            label: 'custom label',
            value: ['a', 'b'],
          },
        },
        'NATIVE_FILTER-bar456': {
          filterState: {
            value: undefined,
          },
        },
      },
    });
    expect(urlWithNativeFilters).toBe(
      'path?preselect_filters=%7B%7D&native_filters=%28NATIVE_FILTER-bar456%3A%28filterState%3A%28value%3A%21n%29%29%2CNATIVE_FILTER-foo123%3A%28filterState%3A%28label%3A%27custom+label%27%2Cvalue%3A%21%28a%2Cb%29%29%29%29',
    );
  });
});
